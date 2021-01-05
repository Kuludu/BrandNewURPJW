<template>
  <div class="container col-md-4">
    <h1>IFTTT成绩推送设置</h1>
    <b-form @submit="submit">
      <b-form-group
          id="event-name-group"
          label-cols="4"
          label="事件名:"
      >
        <b-form-input
            id="event-name-input"
            v-model="push_info.event_name"
            type="text"
            placeholder="事件名"
            required
        ></b-form-input>
      </b-form-group>

      <b-form-group
          id="key-group"
          label-cols="4"
          label="key"
      >
        <b-form-input
            id="key-input"
            v-model="push_info.key"
            type="password"
            placeholder="key"
            required
        ></b-form-input>
      </b-form-group>


      <b-form-group id="push-group">
        <b-form-checkbox
            v-model="push_info.save"
            switch
        >
          是否启用推送？
        </b-form-checkbox>
      </b-form-group>

      <b-button type="submit" variant="primary">提交</b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "Setting",
  props: {
    push_info: {
      event_name: String,
      key: String,
      save: Boolean
    }
  },
  methods: {
    submit: function (event) {
      event.preventDefault()
      this.$parent.updatePush()
    }
  }
}
</script>

<style scoped>

</style>