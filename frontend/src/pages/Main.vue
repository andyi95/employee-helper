<template>
<v-card v-for="vacancy in vacancies" :title="vacancy.name" v-bind:key="vacancy.id" class="mx-auto mt-5">
    <v-card-item title="Комания">{{ vacancy.employer.name }}</v-card-item>
    <v-card-actions><v-btn>Смотреть</v-btn><v-btn icon><v-icon icon="mdi-heart">mdi-heart</v-icon></v-btn></v-card-actions>
</v-card>
</template>

<script>
import {mockedVacancies} from "@/store/mock"
export default {
    name: "Main",
    data(){
        return{
            vacancies: mockedVacancies.items
        }
    }

}

</script>

<style scoped>

</style>