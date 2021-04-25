<template>
  <div id="chart" class="m-5">
    <apexchart
      type="heatmap"
      height="350"
      :options="chartOptions"
      :series="seriesFormat"
    ></apexchart>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from "vuex";
import VueApexCharts from "vue-apexcharts";

export default {
  name: "HeatMap",
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      series: {
        Line1: [0, 0.1, 0.2, 0.4],
        Line2: [0, 0.1, 0.2, 0.4],
        Line3: [0, 0.1, 0.2, 0.4],
        Line4: [0, 0.1, 0.2, 0.4],
        Line5: [0, 0.1, 0.2, 0.4],
        Line6: [0, 0.1, 0.2, 0.4],
        Line7: [0, 0.1, 0.2, 0.4],
        Line8: [0, 0.1, 0.2, 0.4],
        Line9: [0, 0.1, 0.2, 0.4],
        Line10: [0, 0.1, 0.2, 0.4],
        Line11: [0, 0.1, 0.2, 0.4],
        Line12: [0, 0.1, 0.2, 0.4],
      },
      chartOptions: {
        chart: {
          height: 350,
          type: "heatmap",
          foreColor: "#FFFFFF",
        },
        xaxis: {
          label: "Time of day",
          categories: [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
          ],
        },
        dataLabels: {
          enabled: false,
        },
        // colors: ["#008FFB"],
        title: {
          text: "Occupancy over the day",
        },
        plotOptions: {
          heatmap: {
            colorScale: {
              ranges: [
                {
                  from: 0.75,
                  to: 1.0,
                  color: "#aa0000",
                  name: "High Occupancy",
                },
                {
                  from: 0.5,
                  to: 0.75,
                  color: "#aaaa00",
                  name: "Medium Occupancy",
                },
                {
                  from: 0.0,
                  to: 0.5,
                  color: "#00aa00",
                  name: "Low Occupancy",
                },
              ],
            },
          },
        },
      },
    };
  },
  computed: {
    ...mapState(["data"]),
    seriesFormat() {
      let series = [];
      for (const key in this.series) {
        series.push({ name: key, data: this.series[key] });
      }
      return series;
    },
  },
  async mounted() {
    this.update();
    this.$store.dispatch("startAutoUpdate");
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === "addData") {
        // this.update();
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
      let modellMitZweiHoeckern = (hour) =>
        0.1 +
        (0.00002 * (hour + 5) ** 2 * (hour - 30) ** 2) /
          (2 + 0.01 * (hour - 8) ** 2 * (hour - 17) ** 2);
      const hours = [0, ...Array.from(Array(24).keys())];
      const occupancy = hours.map((h) => modellMitZweiHoeckern(h));

      // Standard Normal variate using Box-Muller transform.
      let randn_bm = () => {
        var u = 0,
          v = 0;
        while (u === 0) u = Math.random(); //Converting [0,1) to (0,1)
        while (v === 0) v = Math.random();
        return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
      };

      // console.log("Occupancy: ", occupancy)
      for (const key in this.series) {
        this.series[key] = occupancy.map((v) =>
          Math.min(Math.max(v + 0.05 * randn_bm(), 0.0), 1.0)
        );
      }
    },
    getImgUrl(pic) {
      return require("../assets/" + pic);
    },
  },
};
</script>

<style scoped>
.text {
  color: red;
}

.map {
  width: 60vw;
  min-width: 360px;
  text-align: center;
  margin: 5% auto;
  background-color: #ccc;
}
</style>
