<template>
  <div class="usecase">
    <b-card class="mx-5 my-2" title="Heat Map" sub-title="">
      <HeatMap></HeatMap>
    </b-card>

    <b-card class="mx-5 my-2" title="Map" sub-title="">
      <div class="row">
        <b-list-group class="col-3 mt-5">
          <div v-for="bus in busList" :key="bus.name">
            <b-list-group-item v-on:click="tmp(bus)">
              <BusElement :name="bus.name" :data="bus.data"></BusElement>
            </b-list-group-item>
          </div>
        </b-list-group>
        <div class="col-9">
          <Map></Map>
        </div>
      </div>
    </b-card>
  </div>
</template>

<script>
// @ is an alias to /src
import Map from "@/components/Map.vue";
import { mapState } from "vuex";
import HeatMap from "@/components/Heatmap.vue";
import BusElement from "@/components/BusElement.vue";

export default {
  name: "UseCase",
  components: {
    HeatMap,
    BusElement,
    Map,
  },
  computed: mapState(["data"]),
  created() {
    this.$store.dispatch("startAutoUpdate");
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === "addData") {
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
    tmp(bus) {
      console.log(bus.name);
    },
    cancelAutoUpdate() {
      clearInterval(this.timer);
    },
    update() {
      //   this.configCircle.radius = this.$store.state.data;

      // Get data
      const data = this.$store.state.data;
      // For all lines
      for (let line in data) {
        let lineObj = data[line];
        // console.log(lineObj);
        // For all busses
        for (let bus in lineObj) {
          let busObj = lineObj[bus];
          // Add bus object to list if not available
          if (!this.busList.some((e) => e.name === bus)) {
            this.busList.push({ name: bus, data: busObj });
          }
        }
      }
    },
  },
  data() {
    return {
      busList: [],
      //   configKonva: {
      //     width: 1000,
      //     height: 500,
      //   },
      //   configCircle: {
      //     x: 600,
      //     y: 100,
      //     radius: 20,
      //     fill: "red",
      //     stroke: "black",
      //     strokeWidth: 4,
      //   },
    };
  },
};
</script>

<style scoped>
/* #heat-wrapper {
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
} */
</style>
