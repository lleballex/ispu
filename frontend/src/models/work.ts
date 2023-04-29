import { Comment } from "@/models/comment"
import { PublicTeacher } from "@/models/teacher"
import { PublicStudent } from "@/models/student"

export interface Work {
  id: number
  student: PublicStudent
  name: string
  author: string
  issue: string
  keywords: string[]
  field: string
  tasks: string
  novelty: string
  significance: string
  tools: string
  aprobation: string
  comments: Comment[]
  likes: number
  is_liked: boolean
  message: string // TODO: message only for teacher review
  status: "PENDING" | "ACCEPTED" | "REJECTED"
}

export interface UserWork {
  id: number
  name: string
  teacher: PublicTeacher
  student: PublicStudent
  status: "PENDING" | "ACCEPTED" | "REJECTED"
  message: string
}

export interface UpdateWork {
  id: number
  name: string
  author: string
  teacher: number | null
  issue: string
  novelty: string
  keywords: string[]
  field: string
  tasks: string
  significance: string
  tools: string
  aprobation: string
  tasks_category: number | null
  field_category: number | null
}
