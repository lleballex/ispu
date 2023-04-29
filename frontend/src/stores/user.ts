import { defineStore } from "pinia"

interface StudentProfile {
  id: number
  number: number
  course: number
  group: string
}

interface TeacherProfile {
  id: number
}

export const useUser = defineStore("user", {
  state: () => ({
    isAuthed: false,
    id: 0,
    username: "",
    email: "",
    firstName: "",
    lastName: "",
    patronymic: "",
    studentProfile: null as StudentProfile | null,
    teacherProfile: null as TeacherProfile | null,
  }),
  actions: {
    login(data: any) {
      this.isAuthed = true
      this.id = data.id
      this.username = data.username
      this.email = data.email
      this.firstName = data.first_name
      this.lastName = data.last_name
      this.patronymic = data.patronymic
      this.studentProfile = data.student_profile
      this.teacherProfile = data.teacher_profile
    },
    logout() {
      this.$reset()
    },
  },
})
