<template>
<v-card v-for="vacancy in vacancies" :title="vacancy.name" v-bind:key="vacancy.id" class="mx-auto mt-5">
    <v-card-item title="Комания">{{ vacancy.employer?.name }}</v-card-item>
  <v-card-item title="Опубликована">{{ vacancy.published_at}}</v-card-item>
    <v-card-actions><v-btn>Смотреть</v-btn><v-btn icon><v-icon icon="mdi-heart">mdi-heart</v-icon></v-btn></v-card-actions>
</v-card>
  <v-btn class="mt-5 align-center" @click="load_more">Загрузить ещё</v-btn>
</template>

<script>
// eslint-disable-next-line no-unused-vars
import {mockedVacancies} from "@/store/mock"
import {api} from "@/helpers/api";

export default {
    name: "Main",
    data(){
        return{
            vacancies: null,
          page: 0

        }
    },
  mounted() {
      this.load_data()
  },
  methods:{
      load_data(){
              let page = this.page === 0? 1 : this.page - 1
      api.get('vacancies/', {params: {limit: 10, offset: page * 10}})
          .then(response => {
            this.vacancies = response.data
          }).catch(e => {
            console.log(e)
      })
      },
      load_more(){
        this.page++;
        this.load_data()
  }
  }

}

</script>

<style scoped>

</style>