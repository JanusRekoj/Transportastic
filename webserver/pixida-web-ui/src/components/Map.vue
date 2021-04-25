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
      searchView: true,
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
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === "addData") {
        this.addPolylineToMap([
          [48.1517826, 11.5259065, 100],
          [48.1717826, 11.5459065, 100],
        ]);
        this.updateMap();
      }
    });

    if (this.searchView) {
      // Add markers
      const H = window.H;
      let markerA = new H.map.Marker({ lat: 48.095882, lng: 11.563641 });
      let markerB = new H.map.Marker({ lat: 48.119566, lng: 11.600229 });
      this.map.addObject(markerA);
      this.map.addObject(markerB);

      // Center map view
      this.map.setCenter({ lat: 48.107548, lng: 11.584053 });
      this.map.setZoom(14);

      // Show three routes
      let pointsA = [
        [48.095882, 11.563641, 100],
        [48.09546, 11.566023, 100],
        [48.09336, 11.569993, 100],
        [48.099636, 11.585166, 100],
        [48.102831, 11.597429, 100],
        [48.104526, 11.605188, 100],
        [48.106741, 11.604205, 100],
        [48.110574, 11.603635, 100],
        [48.115846, 11.602101, 100],
        [48.119566, 11.600229, 100],
      ];

      let pointsB = [
        [48.095882, 11.563641, 100],
        [48.098035, 11.564164, 100],
        [48.104657, 11.569804, 100],
        [48.108628, 11.574054, 100],
        [48.111631, 11.576003, 100],
        [48.118025, 11.577111, 100],
        [48.119561, 11.582165, 100],
        [48.117055, 11.589803, 100],
        [48.11959, 11.599958, 100],
        [48.119566, 11.600229, 100],
      ];

      let pointsC = [
        [48.095882, 11.563641, 100],
        [48.09546, 11.566023, 100],
        [48.09336, 11.569993, 100],
        [48.098487, 11.581899, 100],
        [48.103141, 11.582313, 100],
        [48.104337, 11.581541, 100],
        [48.104724, 11.583515, 100],
        [48.104801, 11.589091, 100],
        [48.105942, 11.593117, 100],
        [48.106782, 11.596297, 100],
        [48.110824, 11.594497, 100],
        [48.11222, 11.593143, 100],
        [48.114935, 11.592338, 100],
        [48.117087, 11.590004, 100],
        [48.119566, 11.600229, 100],
      ];

      this.addPolylineToMap(pointsA, "#FF0000");
      this.addPolylineToMap(pointsB, "#00FF00");
      this.addPolylineToMap(pointsC, "#FFFF00");
    }
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
      console.log("LogLogLog!");
      // Get data
      const data = this.$store.state.data;
      console.log("Data: ", data);

      // For all lines
      for (let line in data) {
        let lineObj = data[line];
        // console.log(lineObj);
        // For all busses
        for (let bus in lineObj) {
          let busObj = lineObj[bus];
          console.log("Data: ", busObj);
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
    addPolylineToMap(points, color) {
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
              lineWidth: 10,
              strokeColor: color,
              //   strokeColor: "#A10000",
            //   fillColor: "rgba(0, 85, 170, 0.4)",
              fillColor: "rgba(0, 0, 0, 1)",
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
