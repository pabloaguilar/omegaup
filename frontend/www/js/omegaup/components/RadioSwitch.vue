<template>
  <div class="form-control container-fluid">
    <div class="form-check form-check-inline">
      <label class="form-check-label">
        <input
          class="form-check-input"
          type="radio"
          v-bind:name="name"
          v-bind:value="valueForTrue"
          v-model="radioValue"
          v-on:change.prevent="onUpdateInput"
        />{{ textForTrue }}
      </label>
    </div>
    <div class="form-check form-check-inline">
      <label class="form-check-label">
        <input
          class="form-check-input"
          type="radio"
          v-bind:name="name"
          v-bind:value="valueForFalse"
          v-model="radioValue"
          v-on:change.prevent="onUpdateInput"
        />{{ textForFalse }}
      </label>
    </div>
  </div>
</template>

<script lang="ts">
import { Vue, Component, Prop, Emit, Watch } from 'vue-property-decorator';
import T from '../lang';

@Component
export default class RadioSwitch extends Vue {
  @Prop() name!: string;
  @Prop() selectedValue!: any;
  @Prop({ default: true }) valueForTrue!: any;
  @Prop({ default: false }) valueForFalse!: any;
  @Prop({ default: T.wordsYes }) textForTrue!: string;
  @Prop({ default: T.wordsNo }) textForFalse!: string;

  radioValue = this.selectedValue ?? false;

  @Watch('radioValue')
  @Emit('update:value')
  onUpdateInput(newValue: any): any {
    return newValue;
  }
}
</script>
