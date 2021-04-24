<template>
  <div class="navbar">
    <b-navbar toggleable="sm" type="dark" variant="dark" class="w-100">
      <a href="#" class="navbar-left"><b-img src="../assets/transportastic-logo.svg" class="pr-3" height="30"/></a>
      <!-- <b-navbar-brand href="#">Transportastic</b-navbar-brand> -->

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item to="/">Home</b-nav-item>
          <b-nav-item to="/company">Company</b-nav-item>
          <b-nav-item to="/passenger">Passenger</b-nav-item>
          <b-nav-item to="/team">Team</b-nav-item>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: "NavBar",
  components: {},
};
</script>

<style scoped>
</style>
