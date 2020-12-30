<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <b-container>
      <b-navbar-brand href="#">BrandNewURPJW</b-navbar-brand>
      <div>
        <ul class="navbar-nav mr-auto mt-2 mt-lg-0">
          <li class="nav-item">
            <a class="nav-link">成绩查询</a>
          </li>
          <li class="nav-item">
            <a class="nav-link">考试查询</a>
          </li>
          <li class="nav-item">
            <a class="nav-link">登出</a>
          </li>
        </ul>
      </div>
    </b-container>
  </nav>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    appName: String,
    isLogin: Boolean
  }
}
</script>

<style scoped>

</style>