<template>
  <div class="profile">
    <div class="p-5">
      <b-img
        :src="getImgUrl(this.image)"
        :width="200"
        :height="200"
        :alt="this.name"
        class="m1"
        rounded="circle"
      ></b-img>
      <h1 class="pt-5">{{ this.name }}</h1>
      <h4>{{ this.role }}</h4>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "NavBar",
  components: {},
  props: {
    name: String,
    role: String,
    image: String,
  },
  data() {
    return {};
  },
  methods: {
    getImgUrl(pic) {
      return require("../assets/profile_images/" + pic);
    },
  },
};
</script>

<style scoped>
</style>
