<script setup lang="ts">
import { VisXYContainer, VisLine, VisAxis } from '@unovis/vue';

// Define props to accept `data` from the parent
const props = defineProps<{
  data: { creation_date: string; count: number }[];
}>();

// Map and validate data for the chart
const chartData = props.data
  .map((item) => ({
    date: new Date(item.creation_date).getTime(), // Convert ISO date to timestamp
    count: typeof item.count === "number" ? item.count : NaN,
  }))
  .filter((item) => !isNaN(item.date) && !isNaN(item.count)); // Filter out invalid data

// Debugging: Log input and processed data
console.log("Input Data for Chart:", props.data);
console.log("Processed Chart Data for Chart:", chartData);

// Accessors for the chart
const xAccessor = (d: { date: number }) => new Date(d.date); // Treat x-axis as dates
const yAccessor = (d: { count: number }) => d.count;
</script>

<template>
  <div>
    <!-- Chart Container -->
    <VisXYContainer style="width: 100%; height: 300px;">
      <VisLine :data="chartData" :x="xAccessor" :y="yAccessor" :style="{ stroke: '#0000FF' }" />
      <VisAxis 
        type="x" 
        scale="time" 
        :tickFormat="(d) => new Date(d).toLocaleDateString()" 
        />
      <VisAxis type="y" />
    </VisXYContainer>
  </div>
  
</template>