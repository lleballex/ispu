<template>
  <div class="works">
    <div class="works__header">
      <h1 class="works__title">Мои работы</h1>
      <BaseButton link="works/new">Добавить</BaseButton>
    </div>
    <p v-if="!works?.length" class="works__nothing">Ничего нет</p>
    <table v-else class="works__table">
      <tr class="works__table-head">
        <th>Название разработки</th>
        <th>Научный руководитель</th>
        <th>Статус</th>
        <th>Сообщение</th>
      </tr>
      <tr v-for="(work, idx) in works" class="works__table-row" :key="idx" @click="goToWork(work)">
        <td>{{ work.name }}</td>
        <td>
          {{
            `${work.teacher.last_name} ${work.teacher.first_name[0]}. ${work.teacher.patronymic[0]}.`
          }}
        </td>
        <td>
          <icon
            class="works__table-status-icon"
            :class="work.status.toLowerCase()"
            :icon="getStatusIcon(work)"
          />
        </td>
        <td>{{ work.message || "—" }}</td>
      </tr>
    </table>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import BaseButton from "@/components/base/BaseButton.vue"
import { useFetch } from "@/composables/fetch"
import { UserWork } from "@/models/work"

const works = ref<UserWork[] | null>(null)

useFetch<UserWork[]>("users/works").then((res) => {
  works.value = res.data
  console.log(res.data)
})

const getStatusIcon = (work: UserWork) => {
  if (work.status === "PENDING") {
    return "fa-solid fa-clock"
  } else if (work.status === "ACCEPTED") {
    return "fa-solid fa-circle-check"
  } else {
    return "fa-solid fa-circle-xmark"
  }
}

const router = useRouter()

const goToWork = (work: UserWork) => {
  router.push(`/works/${work.id}`)
}
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.works {
  display: flex;
  flex-direction: column;
  align-self: center;
  gap: 1.5em;
  width: fit-content;
  font-size: 1rem;
}

.works__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2em;
}

.works__title {
  font-size: 2em;
}

.works__nothing {
  margin-top: 2em;
  text-align: center;
}

.works__table {
  max-width: 60em;
  overflow: hidden;
  border-spacing: 0;
  border-radius: $radius;
  text-align: left;
  box-shadow: $shadow;

  th,
  td {
    padding: 1.3em 2.2em;
  }
}

.works__table-head {
  > th {
    background: #b2dfdb;
    white-space: nowrap;
  }
}

.works__table-row {
  cursor: pointer;

  > td {
    transition: $transition;
  }

  &:hover > td {
    background: darken($background-hover, 10%) !important;
  }

  &:nth-child(2n + 1) {
    > td {
      background: $background-hover;
    }
  }
}

.works__table-status-icon {
  &.pending {
    color: #f1c40f;
  }

  &.accepted {
    color: #27ae60;
  }

  &.rejected {
    color: #e74c3c;
  }
}
</style>
