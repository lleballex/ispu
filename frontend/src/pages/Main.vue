<template>
  <div class="works">
    <div class="works__header">
      <h1 class="works__header-title">Каталог инноваций</h1>
      <input
        class="works__header-input"
        v-model="searchQuery"
        type="text"
        placeholder="Поиск по работам"
      />
    </div>
    <div class="works__content">
      <div class="works__filters">
        <div class="works__filter">
          <p>Области применения</p>
          <div class="works__filter-items">
            <div
              v-for="category in fieldCategories"
              class="works__filter-item"
              :class="{ active: aFieldCtgrs.includes(category.id) }"
              :key="category.id"
              @click="() => toggleFieldCategory(category.id)"
            >
              <span class="works__filter-item-checkbox">
                <icon class="works__filter-item-checkbox-icon" icon="fa-solid fa-check" />
              </span>
              <span>{{ category.name }}</span>
            </div>
          </div>
        </div>
        <div class="works__filter">
          <p>Решаемые задачи</p>
          <div class="works__filter-items">
            <div
              v-for="category in tasksCategories"
              class="works__filter-item"
              :class="{ active: aTasksCtgrs.includes(category.id) }"
              :key="category.id"
              @click="() => toggleTasksCategory(category.id)"
            >
              <span class="works__filter-item-checkbox">
                <icon class="works__filter-item-checkbox-icon" icon="fa-solid fa-check" />
              </span>
              <span>{{ category.name }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="loading" class="works__loading">
        <icon icon="fa-solid fa-spinner" spin />
      </div>

      <div v-else-if="!works?.length" class="works__nothing">Ничего нет</div>

      <div v-else class="works__list">
        <RouterLink
          v-for="work in works"
          class="works__work"
          :key="work.id"
          :to="`/works/${work.id}`"
        >
          <p class="works__work-name">{{ work.name }}</p>
          <p>{{ work.issue }}</p>
          <div class="works__work-categories">
            <span class="works__work-category">{{ work.tasks_category.name }}</span>
            <span class="works__work-category">{{ work.field_category.name }}</span>
          </div>
          <Button class="works__work-btn" type="secondary">Подробнее</Button>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue"
import { RouterLink } from "vue-router"
import Button from "@/components/base/BaseButton.vue"
import { useFetch } from "@/composables/fetch"

interface Category {
  id: number
  name: string
}

interface Work {
  id: number
  name: string
  issue: string
  tasks_category: Category
  field_category: Category
}

const loading = ref(false)
const works = ref<Work[] | null>(null)
const tasksCategories = ref<Category[] | null>(null)
const fieldCategories = ref<Category[] | null>(null)

useFetch<Category[]>("works/tasks-categories").then((res) => {
  tasksCategories.value = res.data
})

useFetch<Category[]>("works/field-categories").then((res) => {
  fieldCategories.value = res.data
})

const searchQuery = ref("")
const aTasksCtgrs = ref<number[]>([])
const aFieldCtgrs = ref<number[]>([])

const toggleFieldCategory = (id: number) => {
  const idx = aFieldCtgrs.value.indexOf(id)
  if (idx >= 0) {
    aFieldCtgrs.value.splice(idx, 1)
  } else {
    aFieldCtgrs.value.push(id)
  }

  loadWorks()
}

const toggleTasksCategory = (id: number) => {
  const idx = aTasksCtgrs.value.indexOf(id)
  if (idx >= 0) {
    aTasksCtgrs.value.splice(idx, 1)
  } else {
    aTasksCtgrs.value.push(id)
  }

  loadWorks()
}

const loadWorks = async () => {
  loading.value = true

  const { data, status } = await useFetch<Work[]>("works", {
    params: {
      query: searchQuery.value,
      tasks_categories: aTasksCtgrs.value.join(", "),
      field_categories: aFieldCtgrs.value.join(", "),
    },
  })

  loading.value = false

  if (status == 200) {
    works.value = data
  }
}

loadWorks()

watch(searchQuery, loadWorks)
</script>

<style lang="scss" scoped>
@import "@/assets/css/config";

.works {
  display: flex;
  flex-direction: column;
  gap: 4em;
  font-size: 1rem;
}

.works__header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2em;
  padding: 0 0 2.5em 0;
}

.works__header-title {
  font-size: 2.8em;
  font-family: $thin;
}

.works__header-input {
  width: 50em;
  box-sizing: border-box;
}

.works__content {
  display: flex;
  gap: 3em;
}

.works__filters {
  display: flex;
  flex-direction: column;
  gap: 2em;
  max-width: 20%;
  flex-shrink: 0;
}

.works__filter {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.works__filter-items {
  display: flex;
  flex-direction: column;
  gap: 1em;
}

.works__filter-item {
  display: flex;
  align-items: center;
  gap: 0.5em;
  cursor: pointer;
}

.works__filter-item-checkbox {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 1.5em;
  height: 1.5em;
  border-radius: 0.4em;
  border: 1px solid $secondary;
  transition: $transition;

  .works__filter-item:hover &,
  .works__filter-item.active & {
    background: $secondary;
  }
}

.works__filter-item-checkbox-icon {
  font-size: 1.2em;
  color: $background;
}

.works__loading {
  display: flex;
  justify-content: center;
  flex-grow: 1;
  font-size: 2em;
}

.works__nothing {
  flex-grow: 1;
  text-align: center;
  font-size: 1.1em;
}

.works__list {
  display: flex;
  align-self: flex-start;
  gap: 2.5em;
  flex-wrap: wrap;
  width: 100%;
}

.works__work {
  display: flex;
  flex-direction: column;
  gap: 1.4em;
  padding: 1.5em;
  width: calc(100% / 3 - 2.5em * 2 / 3);
  border-radius: $radius;
  box-shadow: $shadow;
  box-sizing: border-box;
  cursor: default;
}

.works__work-name {
  font-weight: 600;
  font-size: 1.2em;
}

.works__work-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5em 1em;
}

.works__work-category {
  padding: 0.2em 0.5em;
  border-radius: $radius;
  background: $primary;
  color: $background;
  font-size: 0.9em;
}

.works__work-btn {
  margin-top: 0.5em;
  padding: 0.8em;
  font-size: 0.9em;
}
</style>
