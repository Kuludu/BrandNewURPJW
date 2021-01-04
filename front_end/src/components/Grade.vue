<template>
  <div>
    <h1>{{ user }} - {{ training_program }}<small>全部成绩</small></h1>
    <b-table striped hover v-if="grade_info !== null" :fields="grade_fields" :items="grade_info" :tbody-tr-class="rowClass"></b-table>
    <p>
      总通过学分：<b-badge variant="success">{{ pass_point }}</b-badge>
    </p>
    <p>
      总未通过学分：<b-badge variant="danger">{{ fail_point }}</b-badge>
    </p>
    <p>
      GPA（不含选修）：<b-badge variant="light">{{ gpa }}</b-badge>
    </p>
    <p>
      加权平均分（不含选修）：<b-badge variant="light">{{ weighted_average_score }}</b-badge>
    </p>
  </div>
</template>

<script>
export default {
  name: "Grade",
  props: {
    user: String,
    training_program: String,
    grade_info: Array
  },
  data: function() {
    return {
      grade_fields: [
        { key: "course_number", label: "课程号"},
        { key: "course_order_number", label: "课序号"},
        { key: "course_name", label: "课程名（中文）"},
        { key: "credit", label: "学分", sortable: true},
        { key: "course_attribute", label: "课程属性", sortable: true},
        { key: "course_grade", label: "成绩", sortable: true},
        { key: "course_point", label: "对应绩点", sortable: true}
      ]
    };
  },
  methods: {
    rowClass: function (item, type) {
      if (!item || type !== "row") return
      if (item.course_grade >= 90) return "table-success"
      if (item.course_grade < 60) return "table-danger"
    }
  },
  computed: {
    pass_point: function () {
      if (this.grade_info === null)
        return

      let return_pass_point = 0.0
      this.grade_info.forEach(item => {
        if (item.course_grade >= 60)
          return_pass_point += item.credit
      })

      return return_pass_point
    },
    fail_point: function () {
      if (this.grade_info === null)
        return

      let return_fail_point = 0.0
      this.grade_info.forEach(function (item) {
        if (item.course_grade < 60)
          return_fail_point += item.credit
      })

      return return_fail_point
    },
    gpa: function () {
      if (this.grade_info === null)
        return

      let weighted_major_point = 0.0
      let total_major_credit = 0.0
      this.grade_info.forEach(function (item) {
        if (item.course_attribute !== "任选") {
         if (item.course_grade >= 60)
           weighted_major_point += item.course_point * item.credit
          total_major_credit += item.credit
        }
      })

      return weighted_major_point / total_major_credit
    },
    weighted_average_score: function () {
      if (this.grade_info === null)
        return

      let weighted_major_grade = 0.0
      let total_major_credit = 0.0
      this.grade_info.forEach(function (item) {
        if (item.course_attribute !== "任选") {
          if (item.course_grade >= 60)
            weighted_major_grade += item.course_grade * item.credit
          total_major_credit += item.credit
        }
      })

      return weighted_major_grade / total_major_credit
    }
  }
}
</script>

<style scoped>

</style>