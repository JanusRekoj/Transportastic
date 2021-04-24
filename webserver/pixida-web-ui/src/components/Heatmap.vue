<template>
<div id="chart" class="m-5">
      <apexchart
        type="heatmap"
        height="350"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from 'vuex';
import VueApexCharts from "vue-apexcharts";

export default {
  name: "HeatMap",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
        series: [
        {
          name: "Journey 1",
          data: [0, 10, 20, 40],
        },
        {
          name: "Journey 2",
          data: [40, 60, 30, 5],
        },
      ],
      chartOptions: {
        chart: {
          height: 350,
          type: "heatmap",
        },
        dataLabels: {
          enabled: false,
        },
        colors: ["#008FFB"],
        title: {
          text: "HeatMap Chart (Single color)",
        },
      },
    };
  },
  computed: mapState(['data']),
  async mounted() {
    this.$store.dispatch("startAutoUpdate");
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'addData') {
        this.update();
      }
    });
  },
  unmounted() {
    this.$store.dispatch("stopAutoUpdate"); // TODO check which component started and which stopped!
  },
  beforeDestroy() {
    this.unsubscribe();
  },
  methods: {
    update() {
      // const data = this.$store.state.data;
    },
    getImgUrl(pic) {
      return require("../assets/" + pic);
    },
  },
};
</script>

<style scoped>
.map {
  width: 60vw;
  min-width: 360px;
  text-align: center;
  margin: 5% auto;
  background-color: #ccc;
}
</style>
