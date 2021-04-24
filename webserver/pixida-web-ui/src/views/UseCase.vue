<template>
  <div class="usecase">
    <h1>Chart 1</h1>
    <HeatMap></HeatMap>
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
import Map from "@/components/Map.vue";
import { mapState } from 'vuex';
import HeatMap from "@/components/Heatmap.vue";

export default {
  name: "UseCase",
  components: {
    HeatMap,
    Map,
  },
  computed: mapState(['data']),
  created() {
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
      this.configCircle.radius = this.$store.state.data;
    },
  },
  data() {
    return {
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
