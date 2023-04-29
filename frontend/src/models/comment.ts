import { PublicUser } from "@/models/user"

export interface Comment {
  id: number
  user: PublicUser
  text: string
  replies: Comment[]
}
