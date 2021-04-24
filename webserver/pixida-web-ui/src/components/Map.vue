<template>
  <div class="map">
    <div
      id="mapContainer"
      style="height: 600px; width: 100%"
      ref="hereMap"
    ></div>
  </div>
</template>

<script>
// @ is an alias to /src
import { mapState } from "vuex";

export default {
  name: "Map",
  components: {},
  data() {
    return {
      platform: null,
      apikey: "vH87o4DX1yPvgsWOXQyQx0eCBOGai_i9cL7UKz3jdEM",
      busLowIcon: {},
      busMidIcon: {},
      busHighIcon: {},
      map: {},
      markers: [],
      mapInitCenter: { lat: 48.116839, lng: 11.599253 },
      mapInitZoom: 14,
    };
  },
  props: {
    center: Object,
  },
  computed: mapState(["data"]),
  async mounted() {
    // Initialize the platform object:
    const platform = new window.H.service.Platform({
      apikey: this.apikey,
    });
    this.platform = platform;
    this.initializeHereMap();
    this.$store.dispatch("startAutoUpdate");
    // Tutorial has the following in created() {}
    this.unsubscribe = this.$store.subscribe((mutation, state) => {
      if (mutation.type === "addData") {
        this.updateMap();
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
    initializeHereMap() {
      // Rendering map
      const mapContainer = this.$refs.hereMap;
      const H = window.H;
      // Obtain the default map types from the platform object
      var maptypes = this.platform.createDefaultLayers();

      // Instantiate (and display) a map object:
      this.map = new H.Map(mapContainer, maptypes.vector.normal.map, {
        zoom: this.mapInitZoom,
        center: this.mapInitCenter,
      });
      addEventListener("resize", () => this.map.getViewPort().resize());

      // Add behavior control
      new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));

      // Add UI
      H.ui.UI.createDefault(this.map, maptypes);

      // Init marker icon
      this.busIcon = new H.map.Icon(this.getImgUrl("bus.png"), {
        size: { w: 40, h: 48 },
      });

      this.busLowIcon = new H.map.Icon(this.getImgUrl("bus_low.png"), {
        size: { w: 40, h: 48 },
      });

      this.busMediumIcon = new H.map.Icon(this.getImgUrl("bus_medium.png"), {
        size: { w: 40, h: 48 },
      });

      this.busHighIcon = new H.map.Icon(this.getImgUrl("bus_high.png"), {
        size: { w: 40, h: 48 },
      });

      //   // Create all markers
      //   this.markers.bus1 = new H.map.Marker(this.mapInitCenter, {
      //     icon: this.busLowIcon,
      //   });
      //   this.markers.bus2 = new H.map.Marker(this.mapInitCenter, {
      //     icon: this.busMediumIcon,
      //   });
      //   this.markers.bus3 = new H.map.Marker(this.mapInitCenter, {
      //     icon: this.busHighIcon,
      //   });

      //   // Add the marker to the map:
      //   for (const [bus] of Object.entries(this.markers)) {
      //     map.addObject(this.markers[bus]);
      //   }
    },
    addMarker(bus, pos) {
      const H = window.H;
      let marker = new H.map.Marker(pos, {
        icon: this.busIcon,
      });
      this.markers[bus] = marker;
      this.map.addObject(marker);
    },
    updateMap() {
      // Get data
      const data = this.$store.state.data;
      // console.log("Data: ", data);

      // For all lines
      for (let line in data) {
        let lineObj = data[line];
        // console.log(lineObj);
        // For all busses
        for (let bus in lineObj) {
          let busObj = lineObj[bus];
          // console.log(busObj);
          let pos =
            busObj["trajectory"][busObj["trajectory"].length - 1]["position"];
          let gpsPos = { lat: pos.lat, lng: pos.lon };
          let occupancy = busObj["trajectory"]["occupancy"];
          let capacity = busObj["businfo"]["capacity"];
          let ratio = occupancy / capacity;

          if (bus in this.markers) {
            // Update markers
            this.markers[bus].setGeometry(gpsPos);
            let icon = this.busIcon;
            if (ratio > 0.75) {
              icon = this.busHighIcon;
            } else if (ratio > 0.5) {
              icon = this.busMediumIcon;
            } else if (ratio > 0.0) {
              icon = this.busLowIcon;
            }
            this.markers[bus].setIcon(icon);
          } else {
            // Create marker
            this.addMarker(bus, gpsPos);
          }
        }
      }
    },
    getImgUrl(pic) {
      return require("../assets/" + pic);
    },
  },
};
</script>

<style scoped>
.map {
  min-width: 360px;
  text-align: center;
  margin: 5% auto;
  background-color: #ccc;
}
</style>
