<template>
  <div class="profile">
    <div class="p-5 text-center">
      <b-img
        :src="getImgUrl(this.image)"
        :width="200"
        :height="200"
        :alt="this.name"
        class="m1"
        rounded="circle"
      ></b-img>
      <h2 class="pt-5">{{ this.name }}</h2>
      <h5>{{ this.role }}</h5>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "ProfileView",
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
