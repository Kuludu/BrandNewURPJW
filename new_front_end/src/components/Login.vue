<template>
  <div class="container col-md-4">
    <b-form @submit="login">
      <b-form-group
          id="username-group"
          label-cols="4"
          label="用户名（学工号）:"
      >
        <b-form-input
            id="username-input"
            v-model="form.username"
            type="text"
            placeholder="用户名（学工号）"
            required
        ></b-form-input>
      </b-form-group>

      <b-form-group
        id="password-group"
        label-cols="4"
        label="密码："
      >
        <b-form-input
          id="password-input"
          v-model="form.password"
          type="password"
          placeholder="密码"
          required
        ></b-form-input>
      </b-form-group>


      <b-form-group id="save-group">
          <b-form-checkbox
              v-model="form.save"
              switch
          >
            是否保存用户名密码？
          </b-form-checkbox>
      </b-form-group>

      <b-button type="submit" variant="primary">提交</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "Login",
  data: function () {
    return {
      form: {
        username: "",
        password: "",
        save: false
      }
    }
  },
  methods: {
    login: function (event) {
      event.preventDefault()
      alert(JSON.stringify(this.form))
    }
  }
}
</script>

<style scoped>

</style>