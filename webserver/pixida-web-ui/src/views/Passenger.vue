<template>
  <div class="passenger">
    <b-card class="mx-5 my-2" title="Search Journey" sub-title="">
      <div class="row">
        <div class="col-4">
          <JourneySearch></JourneySearch>
          <h5 class="mt-3">Results</h5>
          <b-list-group class="">
            <div v-for="journey in searchResults" :key="journey.id">
              <b-list-group-item class="my-1" v-on:click="onJourneySelected">
                <JourneyItem
                  :name="journey.name"
                  :data="journey.data"
                ></JourneyItem>
              </b-list-group-item>
            </div>
          </b-list-group>
        </div>
        <div class="col-8">
          <Map></Map>
        </div>
      </div>
    </b-card>
  </div>
</template>

<script>
// @ is an alias to /src
import JourneySearch from "@/components/JourneySearch.vue";
import JourneyItem from "@/components/JourneyItem.vue";
import Map from "@/components/Map.vue";

export default {
  name: "Passenger",
  components: {
    JourneySearch,
    JourneyItem,
    Map,
  },
  methods: {
    onJourneySelected(event) {
      event.preventDefault();
      console.log("test");
      // TODO: Highlight journey in map
    },
  },
  data() {
    return {
      searchResults: [
        {
          id: 1,
          name: "j1",
          data: {
            startTime: "7:30",
            endTime: "7:55",
            transport: "bus_53",
            occupancy: 1,
            benefit: "+0km",
          },
        },
        {
          id: 2,
          name: "j2",
          data: {
            startTime: "7:40",
            endTime: "8:00",
            transport: "tram_20",
            occupancy: 0.75,
            benefit: "+1.67km",
          },
        },
        {
          id: 3,
          name: "j3",
          data: {
            startTime: "8:00",
            endTime: "8:30",
            transport: "bus_56",
            occupancy: 0.3,
            benefit: "+4.67km",
          },
        },
      ],
    };
  },
};
</script>

<style scoped>
</style>
