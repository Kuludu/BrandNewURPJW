<template>
  <div id="app">
    <Navbar />
    <Login v-show="false"/>
    <Grade />
    <Footer />
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import Login from "@/components/Login";
import Footer from "@/components/Footer";
import Grade from "@/components/Grade";

export default {
  name: 'App',
  components: {
    Grade,
    Footer,
    Login,
    Navbar
  },
  methods: {

  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
