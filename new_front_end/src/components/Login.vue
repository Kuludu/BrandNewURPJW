<template>
  <b-container>
    <br>
    <b-row>
      <b-col offset="3" cols="6">
        <b-input-group size="lg">
          <b-input-group-text>用户名（学工号）</b-input-group-text>
          <b-form-input type="text" v-model="username" placeholder="用户名（学工号）"></b-form-input>
        </b-input-group>
      </b-col>
    </b-row>
    <br>
    <b-row>
      <b-col offset="3" cols="6">
        <b-input-group size="lg">
          <b-input-group-text>密码</b-input-group-text>
          <b-form-input type="password" v-model="password" placeholder="密码"></b-form-input>
        </b-input-group>
      </b-col>
    </b-row>
    <br>
    <b-row>
      <b-col offset="3" cols="6">
        <b-form-checkbox v-model="save" switch>
          保存账号密码？
        </b-form-checkbox>
      </b-col>
    </b-row>
    <br>
    <b-row>
      <b-col offset="3" cols="6">
        <b-button variant="success" @click="login">登录</b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: "Login",
  data: function () {
    return {
      username: "",
      password: "",
      save: "checked"
    }
  },
  methods: {
    login: function () {

    }
  }
}
</script>

<style scoped>

</style>