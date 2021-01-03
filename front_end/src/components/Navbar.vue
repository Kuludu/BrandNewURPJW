<template>
  <b-navbar>
    <b-navbar-brand href="#">BrandNewURPJW</b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-nav-item href="#">成绩查询</b-nav-item>
      <b-nav-item href="#">考试查询</b-nav-item>
      <b-nav-item-dropdown v-if="isLogin" right>
        <template #button-content>
          <em>User</em>
        </template>
        <b-dropdown-item href="#">设置</b-dropdown-item>
        <b-dropdown-item href="#">登出</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    user: String,
    isLogin: Boolean
  }
}
</script>

<style scoped>

</style>