<template>
  <b-navbar>
    <b-navbar-brand href="#">BrandNewURPJW</b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-nav-item href="#">成绩查询</b-nav-item>
      <b-nav-item href="#">考试查询</b-nav-item>
      <b-nav-item v-if="isLogin" href="#">登出</b-nav-item>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    isLogin: Boolean
  }
}
</script>

<style scoped>

</style>