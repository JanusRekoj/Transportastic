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
import { mapState } from 'vuex';

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
      markers: {
        bus1: {},
        bus2: {},
      },
      mapInitCenter: { lat: 48.116839, lng: 11.599253 },
      mapInitZoom: 13,
      occ: 0,
      map: null,
    };
  },
  props: {
    center: Object,
  },
  computed: mapState(['data']),
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
      if (mutation.type === 'addData') {
        this.addPolylineToMap([(48.1517826,11.5259065), (48.1717826,11.5459065)]);
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

      // Create all markers
      this.markers.bus1 = new H.map.Marker(this.mapInitCenter, {
        icon: this.busLowIcon,
      });
      this.markers.bus2 = new H.map.Marker(this.mapInitCenter, {
        icon: this.busMediumIcon,
      });
      this.markers.bus3 = new H.map.Marker(this.mapInitCenter, {
        icon: this.busHighIcon,
      });

      // Add the marker to the map:
      for (const [bus] of Object.entries(this.markers)) {
        this.map.addObject(this.markers[bus]);
      }
      //   this.markers.forEach(m => map.addObject(m))
      //   map.addObject(this.markers.bus1);
      //   map.addObject(this.markers.bus2);
      //   map.addObject(this.markers.bus3);

      // Highlight route
      //   var router = this.platform.getRoutingService(),
      //     routeRequestParams = {
      //       mode: "fastest;car",
      //       representation: "display",
      //       routeattributes: "waypoints,summary,shape,legs",
      //       maneuverattributes: "direction,action",
      //       waypoint0: "48.116839,11.599253",
      //       waypoint1: "48.116939,11.599373",
      //     };

      //   router.calculateRoute(routeRequestParams, {}, {});
    },
    updateMap() {
      //const data = this.$store.state.data
      //console.log("Data: ", data);

      // Update markers
      // Position
      let l = this.markers.bus1.getGeometry();
      //   console.log(l);
      this.markers.bus1.setGeometry({ lat: l.lat + 0.0001, lng: l.lng });

      // Icon (Occupancy)
      this.occ += 10;
      this.occ = this.occ % 100;
      let icon = this.busIcon;

      if (this.occ > 75) {
        icon = this.busHighIcon;
      } else if (this.occ > 50) {
        icon = this.busMediumIcon;
      } else if (this.occ > 0) {
        icon = this.busLowIcon;
      }

      this.markers.bus1.setIcon(icon);
    },
    addPolylineToMap(points) {
      const H = window.H;
      var lineString = new H.geo.LineString();


      for (const pt in points) {
        lineString.pushPoint({lat:pt[0], lng:pt[1]}); // pt[2] is occupancy
      }

      this.map.addObject(new H.map.Polyline(
        lineString, { style: { lineWidth: 4 }}
      ));
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
