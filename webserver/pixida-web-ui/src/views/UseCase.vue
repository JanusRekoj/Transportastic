<template>
  <div class="usecase">
    <h1>Chart 1</h1>
    <div id="chart" class="m-5">
      <apexchart
        type="heatmap"
        height="350"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </div>
    <h1>Chart 2</h1>
    <div id="heat-wrapper">
      <div id="heat-overlay" class="text-center">
        <v-stage :config="configKonva">
          <v-layer>
            <v-circle :config="configCircle"></v-circle>
          </v-layer>
        </v-stage>
      </div>
      <div id="heat-image" class="text-center">
        <img src="@/assets/bus_view.jpg" />
      </div>
    </div>
    <h1>Chart 3</h1>
    <Map></Map>
  </div>
</template>

<script>
// @ is an alias to /src
import VueApexCharts from "vue-apexcharts";
import axios from "axios";
import Map from "@/components/Map.vue";

export default {
  name: "UseCase",
  components: {
    apexchart: VueApexCharts,
    Map,
  },
  created() {
    // this.timer = setInterval(this.autoUpdate, 750);
  },
  methods: {
    autoUpdate() {
      const endtime = new Date('2021-04-12 09:23:22')
      let starttime = endtime;
      let durationInMinutes = 1;
      starttime.setMinutes(endtime.getMinutes() - durationInMinutes);
      const params = {
       start: starttime.getTime(),
       end: endtime.getTime(),
       line: 'trip_1',
       // bus: 'bus_trip_1',
       // station: 
      };
     axios.get('/data', { params }).then(
        (result) => {
          // console.log("Data: ", result.data);
          this.configCircle.radius = result.data;
        },
        (error) => {
          console.error(error);
        }
      );
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },
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
      configKonva: {
        width: 1000,
        height: 500,
      },
      configCircle: {
        x: 600,
        y: 100,
        radius: 20,
        fill: "red",
        stroke: "black",
        strokeWidth: 4,
      },
    };
  },
};
</script>

<style scoped>
#heat-wrapper {
  position: relative;
  width: 100%;
}

#heat-image {
  width: 100%;
}

#heat-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0%;
  /* background-color: red; */
}
</style>
