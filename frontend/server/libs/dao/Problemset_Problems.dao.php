<?php

include('base/Problemset_Problems.dao.base.php');
include('base/Problemset_Problems.vo.base.php');
/** ProblemsetProblems Data Access Object (DAO).
  *
  * Esta clase contiene toda la manipulacion de bases de datos que se necesita para
  * almacenar de forma permanente y recuperar instancias de objetos {@link ProblemsetProblems }.
  * @access public
  *
  */
class ProblemsetProblemsDAO extends ProblemsetProblemsDAOBase
{
    final public static function getProblems($problemset_id) {
        // Build SQL statement
        $sql = 'SELECT p.title, p.alias, p.time_limit, p.overall_wall_time_limit, '.
               'p.memory_limit, p.languages, pp.points, pp.order ' .
               'FROM Problems p ' .
               'INNER JOIN Problemset_Problems pp ON pp.problem_id = p.problem_id ' .
               'WHERE pp.problemset_id = ? ' .
               'ORDER BY pp.`order` ASC;';
        $val = array($problemset_id);

        global $conn;
        return $conn->GetAll($sql, $val);
    }
}
