import { defineStore } from "pinia"

interface StudentProfile {
  number: number
}

interface TeacherProfile {}

export const useUser = defineStore("user", {
  state: () => ({
    isAuthed: false,
    email: "",
    firstName: "",
    lastName: "",
    studentProfile: null as StudentProfile | null,
    teacherProfile: null as TeacherProfile | null,
  }),
  actions: {
    login(data: any) {
      this.isAuthed = true
      this.email = data.email
      this.firstName = data.first_name
      this.lastName = data.last_name
      this.studentProfile = data.student_profile
      this.teacherProfile = data.teacher_profile
    },
    logout() {
      this.$reset()
    },
  },
})
