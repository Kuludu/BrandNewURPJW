<template>
  <b-navbar>
    <b-navbar-brand href="#">BrandNewURPJW</b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-nav-item v-on:click="$emit('showGrade')">成绩查询</b-nav-item>
      <b-nav-item-dropdown v-if="user !== null" right>
        <template #button-content>
          <em>{{ user }}({{ username }})</em>
        </template>
        <b-dropdown-item v-on:click="$emit('showSetting')">设置</b-dropdown-item>
        <b-dropdown-item v-on:click="$emit('onLogout')">登出</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    user: String,
    username: String
  }
}
</script>

<style scoped>

</style>