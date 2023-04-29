<template>
  <div class="works">
    <p v-if="!works?.length">Ничего нет</p>
    <table v-else class="works__table">
      <tr class="works__table-head">
        <th>Название разработки</th>
        <th>Автор</th>
        <th>Статус</th>
        <th>Сообщение</th>
      </tr>
      <tr
        v-for="work in works"
        class="works__table-row"
        :key="work.id"
        @click="() => goToWork(work)"
      >
        <td>{{ work.name }}</td>
        <td class="works__table-author">
          {{
            `${work.student.last_name} ${work.student.first_name[0]}. ${work.student.patronymic[0]}.`
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
import { UserWork } from "@/models/work"
import { useFetch } from "@/composables/fetch"

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
  if (work.status === "ACCEPTED") {
    router.push(`/works/${work.id}`)
  } else {
    router.push(`/works/${work.id}/review`)
  }
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

.works__table-author {
  white-space: nowrap;
}
</style>
