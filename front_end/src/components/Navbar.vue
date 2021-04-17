<template>
  <b-navbar>
    <b-navbar-brand href="#">BrandNewURPJW</b-navbar-brand>
    <b-navbar-nav class="ml-auto">
      <b-nav-item v-if="user !== null" @click="onShowGrade">成绩查询</b-nav-item>
      <b-nav-item v-if="user !== null" @click="onExportSchedule">课表导出</b-nav-item>
      <b-nav-item-dropdown v-if="user !== null" right text="设置">
        <b-dropdown-item @click="onShowSetting">推送设置</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>
  </b-navbar>
</template>

<script>
export default {
  name: "Navbar",
  props: {
    user: String
  },
  methods: {
    onShowGrade() {
      this.$parent.showGrade()
    },
    onShowSetting() {
      this.$parent.showSetting()
    },
    onExportSchedule() {

    }
  }
}
</script>

<style scoped>

</style>