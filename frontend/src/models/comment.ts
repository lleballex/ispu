import { PublicUser } from "@/models/user"

export interface Comment {
  id: number
  user: PublicUser
  work: number
  text: string
  replies: Comment[]
  reply_to: string
}
