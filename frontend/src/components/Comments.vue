<template>
  <div class="comments">
    <div class="comments__icons">
      <div class="comments__icon btn" :class="{ like: work.is_liked }" @click="toggleLike">
        <icon
          class="comments__icon-icon"
          :icon="`fa-${work.is_liked ? 'solid' : 'regular'} fa-heart`"
        />
        <span>{{ work.likes }}</span>
      </div>
      <div class="comments__icon">
        <icon class="comments__icon-icon" icon="fa-regular fa-comment" />
        <span>{{ work.comments_count }}</span>
      </div>
    </div>
    <form class="comments__form" @submit.prevent="sendComment">
      <img class="comments__user-img" src="@/assets/images/user.svg" />
      <div class="comments__form-input-container">
        <span
          v-if="newComment.replyTo"
          class="comments__form-input-reply"
          @click="cancelReplyToComment"
          >{{ newComment.replyTo.user.first_name }} {{ newComment.replyTo.user.last_name }}
        </span>
        <input
          class="comments__form-input"
          v-model="newComment.text"
          type="text"
          placeholder="Комментарий"
        />
      </div>
      <icon @click="sendComment" class="comments__form-icon" icon="fa-solid fa-paper-plane" />
    </form>
    <div class="comments__list">
      <div v-for="comment in work.comments" class="comments__comment-container" :key="comment.id">
        <div class="comments__comment">
          <img class="comments__user-img" src="@/assets/images/user.svg" />
          <div class="comments__comment-info">
            <p class="comments__user-name">
              {{ comment.user.first_name }} {{ comment.user.last_name }}
            </p>
            <p class="comments__comment-text">{{ comment.text }}</p>
          </div>
          <div class="comments__comment-actions">
            <icon
              class="comments__comment-action"
              icon="fa-solid fa-reply"
              @click="() => replyToComment(comment, comment)"
            />
            <icon
              v-if="comment.user.id === user.id"
              class="comments__comment-action"
              icon="fa-solid fa-trash"
              @click="() => deleteComment(comment)"
            />
          </div>
        </div>
        <Button
          v-if="comment.replies.length && !comment.areRepliesShowed"
          class="comments__comment-replies-btn"
          @click="() => (comment.areRepliesShowed = true)"
          type="text"
          >Ответы ({{ comment.replies.length }})</Button
        >
        <div
          v-else-if="comment.replies.length && comment.areRepliesShowed"
          class="comments__list"
          style="margin-left: 3.5em"
        >
          <div v-for="reply in comment.replies" class="comments__comment" :key="reply.id">
            <img class="comments__user-img" src="@/assets/images/user.svg" />
            <div class="comments__comment-info">
              <p class="comments__user-name">
                {{ reply.user.first_name }} {{ reply.user.last_name }}
              </p>
              <p class="comments__comment-text">{{ reply.reply_to }}, {{ reply.text }}</p>
            </div>
            <div class="comments__comment-actions">
              <icon
                class="comments__comment-action"
                icon="fa-solid fa-reply"
                @click="() => replyToComment(reply, comment)"
              />
              <icon
                v-if="reply.user.id === user.id"
                class="comments__comment-action"
                icon="fa-solid fa-trash"
                @click="() => deleteComment(reply)"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { reactive } from "vue"
import { notify } from "@kyvg/vue3-notification"
import { useUser } from "@/stores/user"
import { Work } from "@/models/work"
import { useFetch } from "@/composables/fetch"
import { Comment } from "@/models/comment"
import Button from "./base/BaseButton.vue"

const { work } = defineProps<{
  work: Work
}>()

const user = useUser()

const newComment = reactive({
  text: "",
  baseComment: null as Comment | null,
  replyTo: null as Comment | null,
})

const toggleLike = async () => {
  if (!user.isAuthed) {
    return notify({
      type: "error",
      text: "Сначала надо авторизоваться",
    })
  }

  const { status, data } = await useFetch<{
    likes: number
    is_liked: boolean
  }>(`works/${work.id}/like`, {
    method: "POST",
  })

  if (status == 200) {
    if (data) {
      work.likes = data?.likes
      work.is_liked = data?.is_liked
    }
  } else {
    notify({
      type: "error",
      text: "Что-то пошло не так",
    })
  }
}

const sendComment = async () => {
  if (!user.isAuthed) {
    return notify({
      type: "error",
      text: "Сначала надо авторизоваться",
    })
  }

  const { status, data } = await useFetch<Comment>(`works/comment`, {
    method: "POST",
    body: {
      work: work.id,
      text: newComment.text,
      base_comment: newComment.baseComment?.id,
      reply_to: newComment.replyTo?.id,
    },
  })

  if (status == 201) {
    newComment.text = ""
    newComment.baseComment = null
    newComment.replyTo = null
    if (data)
      work.comments.unshift({
        id: data.id,
        text: data.text,
        replies: [],
        user: {
          id: user.id,
          first_name: user.firstName,
          last_name: user.lastName,
          patronymic: user.patronymic,
        },
      })
  } else {
    notify({
      type: "error",
      text: "Что-то пошло не так",
    })
  }
}

const deleteComment = async (comment: Comment) => {
  if (confirm("Точно удалить комментарий? Восстановить его будет невозможно")) {
    const { status } = await useFetch(`works/comments/${comment.id}`, {
      method: "DELETE",
    })

    if (status !== 204) {
      notify({ type: "error", text: "Что-то пошло не так" })
    } else {
      work.comments.splice(work.comments.indexOf(comment), 1)
    }
  }
}

const replyToComment = (comment: Comment, baseComment: Comment) => {
  newComment.replyTo = comment
  newComment.baseComment = baseComment
}

const cancelReplyToComment = () => {
  newComment.replyTo = null
  newComment.baseComment = null
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.comments {
  display: flex;
  flex-direction: column;
  gap: 2.2em;
  margin-top: 0.3em;
  font-size: 1rem;
}

.comments__icons {
  display: flex;
  align-items: stretch;
  gap: 1em;
}

.comments__icon {
  display: flex;
  align-items: center;
  gap: 0.4em;
  padding: 0.5em 0.8em;
  border-radius: 10em;
  background: #ececec;
  transition: $transition;

  &.btn:hover {
    background: #ddd;
    cursor: pointer;
  }

  &.like {
    background: #ffd8d4 !important;
  }
}

.comments__icon-icon {
  font-size: 1.3em;
  transition: $transition;

  .comments__icon.btn:hover & {
    transform: scale(1.2);
  }

  .comments__icon.like & {
    color: #e74c3c;
  }
}

.comments__form {
  display: flex;
  align-items: center;
  gap: 1em;
}

.comments__form-input-container {
  display: flex;
  align-items: center;
  gap: 0.5em;
  padding: 0 1em;
  width: 100%;
  border: 2px solid $secondary;
  border-radius: 10em;
}

.comments__form-input-reply {
  padding: 0.3em 0.5em;
  margin-left: -0.6em;
  background: #ececec;
  white-space: nowrap;
  border-radius: 10em;
  font-size: 0.9em;
  transition: $transition;

  &:hover {
    background: #ddd;
    cursor: pointer;
  }
}

.comments__form-input {
  padding: 0.7em 0;
  width: 100%;
  border: none;
  background: none;

  &:after {
    content: "sdfsss";
  }
}

.comments__form-icon {
  margin-left: 0.2em;
  font-size: 1.2em;
  color: $primary-simple;
  transition: $transition;

  &:hover {
    transform: scale(1.2);
    cursor: pointer;
  }
}

.comments__user-img {
  width: 2.5em;
  height: 2.5em;
  border-radius: 50%;
}

.comments__list {
  display: flex;
  flex-direction: column;
  gap: 1.6em;
}

.comments__comment-container {
  display: flex;
  flex-direction: column;
  gap: inherit;
}

.comments__comment {
  display: flex;
  gap: 1em;
}

.comments__comment-info {
  display: flex;
  flex-direction: column;
  gap: 0.3em;
}

.comments__user-name {
  font-size: 0.9em;
  font-weight: 600;
}

.comments__comment-text {
}

.comments__comment-actions {
  display: flex;
  align-items: center;
  align-self: flex-start;
  gap: 1em;
  margin-left: auto;
}

.comments__comment-action {
  color: #ccc;
  font-size: 0.9em;
  transition: $transition;

  &:hover {
    transform: scale(1.2);
    cursor: pointer;
  }
}

.comments__comment-replies-btn {
  margin: -1em 0 0 3.5em;
  align-self: flex-start;
}
</style>
