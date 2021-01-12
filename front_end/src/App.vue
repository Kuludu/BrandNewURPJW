<template>
  <div id="app">
    <Navbar :user="name" :username="username" />
    <Login v-show="login_visible" />
    <Grade v-show="grade_visible" :user="name" :username="username" :training_program="major" :grade_info="grade_info" />
    <Setting v-show="setting_visible" :push_info="push_info" />
    <Footer/>
  </div>
</template>

<script>
import Navbar from "@/components/Navbar";
import Login from "@/components/Login";
import Footer from "@/components/Footer";
import Grade from "@/components/Grade";
import qs from "qs";
import Setting from "@/components/Setting";

export default {
  name: 'App',
  components: {
    Setting,
    Grade,
    Footer,
    Login,
    Navbar
  },
  data: function () {
    return {
      token: "",
      login_visible: true,
      grade_visible: false,
      setting_visible: false,
      username: null,
      name: null,
      major: null,
      college: null,
      grade_info: null,
      push_info: {
        event_name: "",
        key: "",
        save: false
      }
    };
  },
  methods: {
    performLogin: function (loginInfo) {
      this.axios({
        method: "post",
        url: this.API.server + '/api/login',
        data: qs.stringify({
          username: loginInfo['username'],
          password: loginInfo['password']
        })
      }).then(resp => {
        this.token = resp.data.token
        this.username = loginInfo['username']
        this.updateInterface()
        this.showGrade()
      }).catch(() => {
        alert("后端服务器错误！")
        this.showLogin()
      })
    },
    updateInterface: function () {
      this.axios({
        method: "post",
        url: this.API.server + '/api/info',
        data: qs.stringify({
          token: this.token
        })
      }).then(resp => {
        this.name = resp.data.name
        this.college = resp.data.college
        this.major = resp.data.major
        this.grade_info = resp.data.grades
        this.push_info = {
          event_name: resp.data.event_name,
          key: resp.data.key,
          save: (resp.data.event_name != null && resp.data.key !== null)
        }

        this.grade_info.forEach( item => {
          item.course_grade = Number(item.course_grade)
          item.credit = Number(item.credit)
          item.course_point = this.calculate_point(item.course_grade)
        })
      }).catch(() => {
        this.showLogin()
        alert("后端服务器错误！")
      })
    },
    updatePush: function () {
      let data = qs.stringify({
        token: this.token
      })
      if (this.push_info['save'] === true) {
        data = qs.stringify({
          token: this.token,
          event_name: this.push_info['event_name'],
          key: this.push_info['key']
        })
      }
      console.log(data)
      this.axios({
        method: "post",
        url: this.API.server + '/api/push',
        data: data
      }).then(function () {
        alert('成功！')
      }).catch(function () {
        alert("后端服务器错误！")
      })
    },
    showGrade: function () {
      this.login_visible = false
      this.setting_visible = false
      this.grade_visible = true
    },
    showSetting: function () {
      this.grade_visible = false
      this.login_visible = false
      this.setting_visible = true
    },
    showLogin: function () {
      this.grade_visible = false
      this.setting_visible = false
      this.login_visible = true
    },
    calculate_point: function (score) {
      if (score >= 90) {
        return 4.0
      } else if (85 <= score && score < 90) {
        return 3.7
      } else if (82 <= score && score < 85) {
        return 3.3
      } else if (78 <= score && score < 82) {
        return 3.0
      } else if (75 <= score && score < 78) {
        return 2.7
      } else if (71 <= score && score < 75) {
        return 2.3
      } else if (66 <= score && score < 71) {
        return 2.0
      } else if (62 <= score && score < 66) {
        return 1.7
      } else if (60 <= score && score < 62) {
        return 1.3
      } else {
        return 0.0
      }
    }
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
