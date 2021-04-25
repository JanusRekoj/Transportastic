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
      // console.log("LogLogLog!");
      if (mutation.type === "addData") {
        this.addPolylineToMap([
          [48.1517826, 11.5259065, 100],
          [48.1717826, 11.5459065, 100],
        ]);
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
      this.busIcon = new H.map.Icon(this.getImgUrl("bus.svg"), {
        size: { w: 40, h: 48 },
      });

      this.busLowIcon = new H.map.Icon(this.getImgUrl("bus_low.svg"), {
        size: { w: 40, h: 48 },
      });

      this.busMediumIcon = new H.map.Icon(this.getImgUrl("bus_medium.svg"), {
        size: { w: 40, h: 48 },
      });

      this.busHighIcon = new H.map.Icon(this.getImgUrl("bus_high.svg"), {
        size: { w: 40, h: 48 },
      });
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

      // For all lines
      for (let line in data) {
        let lineObj = data[line];
        // For all busses
        for (let bus in lineObj) {
          let busObj = lineObj[bus];
          console.log("Bus object: ", busObj);
          let numTrajectory = busObj["trajectory"].length
          if (numTrajectory < 1) {
            console.log("Error: No trajectories in trajectory: ", busObj["trajectory"])
            continue
          } else {
            console.log("Success!! Trajectory has ", numTrajectory, " positions");
          }
          let pos = busObj["trajectory"][numTrajectory - 1]["position"];
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
    addPolylineToMap(points) {
      const H = window.H;

      let connection = [];
      for (let i = 1; i < points.length; i++) {
        connection.push([
          points[i - 1][0],
          points[i - 1][1],
          points[i][0],
          points[i][1],
          points[i][2],
        ]);
      }

      connection.forEach((pt) => {
        let lineString = new H.geo.LineString();
        lineString.pushPoint({ lat: pt[0], lng: pt[1] });
        lineString.pushPoint({ lat: pt[2], lng: pt[3] });
        // TODO use pt[4] for color
        this.map.addObject(
          new H.map.Polyline(lineString, {
            style: {
              lineWidth: 4,
              strokeColor: "#A10000",
              fillColor: "rgba(0, 85, 170, 0.4)",
            },
            zIndex: 0,
          })
        );
      });
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
