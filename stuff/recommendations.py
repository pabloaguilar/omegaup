import apache_beam as beam
import argparse
import sqlite3
import sys
import timeit
from apache_beam.options.pipeline_options import PipelineOptions


def Rekey(run):
  user_id = run[0]
  problem_id = run[1]
  timestamp =  run[2]
  return '%s:%s' % (user_id, problem_id), timestamp


def KeepFirstRun(runs):
  user_and_problem, timestamps = runs
  output = (user_and_problem, min(timestamps))
  return output


def UnpackUserAndProblem(userproblem_timestamp):
  userproblem, timestamp = userproblem_timestamp
  user, problem = map(int, userproblem.split(':'))
  return (user, (problem, timestamp))


output = []  
def collect(run):
  output.append(run)
  return run


def EmitProblemPairs(user_and_problems):
  user, problems = user_and_problems
  n = len(problems)
  problems.sort(key=lambda pt: pt[1])
  if n > 1:
    for i in xrange(n - 1):
      yield (problems[i][0], problems[i+1][0]), 1


def RepackProblemCounts(up_c):
  up, c = up_c
  return up[0], (up[1], c)


def ComputeProbabilitie(s_tc):
  total = 0
  source, target_counts = s_tc
  for target, count in target_counts:
    total += count
  return (source,
          map(lambda tc: (tc[0], float(tc[1]) / total),
              sorted(target_counts, reverse=True, key=lambda tc: tc[1])))


def GetRunsCursor(input_file, num_records):
  conn = sqlite3.connect(input_file)
  cursor = conn.cursor()
  cursor.execute("""
      SELECT
        user_id, problem_id, strftime('%%s', time) as time
      FROM
        Runs
      WHERE 
            verdict = 'AC' 
        AND problemset_id IS NULL
      LIMIT %s
      """ % num_records)
  return cursor


def main(argv):
  parser = argparse.ArgumentParser()
  parser.add_argument('--input',
                      help='Input for the pipeline',
                      default='omegaup.clean_1.db')
  parser.add_argument('--output',
                      help='Output for the pipeline',
                      default='output.txt')
  parser.add_argument('--num_records',
                      help='Number of records to scan',
                      default=1000,
                      type=int)
  known_args, pipeline_args = parser.parse_known_args(argv)
  print known_args
  
  p = beam.Pipeline(argv=pipeline_args)
  cursor = GetRunsCursor(known_args.input, known_args.num_records)
  runs = (p
      | "ReadFromDB" >> beam.Create(cursor)
      | beam.Map(Rekey)
      | "GroupByUserAndProblem" >> beam.GroupByKey()
      | beam.Map(KeepFirstRun)
      | beam.Map(UnpackUserAndProblem)
      | "GroupByUser" >> beam.GroupByKey()
      | beam.ParDo(EmitProblemPairs)
      | beam.CombinePerKey(sum)
      | beam.Map(RepackProblemCounts)
      | "GroupByProblemPair" >> beam.GroupByKey()
      | beam.Map(ComputeProbabilitie)
      #| beam.Map(collect)
      | "WriteOutput" >> beam.io.WriteToText(known_args.output)
  )
  result = p.run()
  result.wait_until_finish()
  print output

total_time = timeit.timeit(lambda: main(sys.argv), number=1)
print "Total time: %.2f seconds" % total_time