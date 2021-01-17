<template>
  <div class="container col-md-4">
    <b-form @submit="login">
      <b-form-group
          id="username-group"
          label="用户名（学工号）:"
          label-cols="4"
      >
        <b-form-input
            id="username-input"
            v-model="form.username"
            placeholder="用户名（学工号）"
            required
            type="text"
        ></b-form-input>
      </b-form-group>

      <b-form-group
          id="password-group"
          label="密码："
          label-cols="4"
      >
        <b-form-input
            id="password-input"
            v-model="form.password"
            placeholder="密码"
            required
            type="password"
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
  created() {
    if (Boolean(this.$cookies.get("save")) === true) {
      this.form.username = this.$cookies.get("username")
      this.form.password = this.$cookies.get("password")
      this.form.save = true
    }
  },
  methods: {
    login: function (event) {
      event.preventDefault()
      if (this.form.save === true) {
        this.$cookies.set("username", this.form.username)
        this.$cookies.set("password", this.form.password)
        this.$cookies.set("save", true)
      } else {
        this.$cookies.remove("username")
        this.$cookies.remove("password")
        this.$cookies.remove("save")
      }

      this.$parent.performLogin({
        username: this.form.username,
        password: this.form.password
      })
    }
  }
}
</script>

<style scoped>

</style>