<template>
  <div class="about">
    <h1 class="display-3 mx-5" >Team</h1>
    <div class="row mx-3">
      <div v-for="dev in developers" :key="dev.name" class="col-lg-4 col-md-6">
        <profile-view :name="dev.name" :role="dev.role" :image="dev.image" />
      </div>
    </div>
    <h1 class="display-3 mx-5" >Partners</h1>
    <div>
        <img class="m-3" height="50" center src="../assets/tum-logo.png" />
        <img class="m-3" height="50" center src="../assets/lmu-logo.png" />
        <img class="m-3" height="50" center src="../assets/pixida-logo.png" />
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import ProfileView from "@/components/ProfileView.vue";

export default {
  name: "About",
  components: {
    ProfileView,
  },
  data() {
    return {
      developers: [
        {
          name: "Michael Maas",
          role: "Team Leader",          
          image: "michael.jpg",
        },
        {
          name: "Johann Brenner",
          role: "Frontend Dev",
          image: "johann.jpg",
        },
        {
          name: "Andreas Finkenzeller",
          role: "Frontend Dev",
          image: "andreas.png",
        },
        {
          name: "Daniel Milz",
          role: "Backend Dev",
          image: "daniel.jpg",
        },
        {
          name: "Alexander Schmaus",
          role: "Backend Dev",
          image: "alexander.jpg",
        },
        {
          name: "Nika Nizharadze",
          role: "Backend Dev",
          image: "nika.jpg",
        },
      ],
    };
  },
};
</script>

<style scoped>
p {
  text-align: justify;
}
</style>