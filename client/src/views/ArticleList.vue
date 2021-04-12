<template>
  <v-container>
    <v-list
      subheader
      two-line
    >
      <v-subheader inset>Recent Articles</v-subheader>

      <v-list-item
        v-for="item in articles"
        :key="item.id"
      >
        <v-list-item-avatar>
          <v-icon
            class="grey lighten-1"
            dark
          >
            mdi-account-circle
          </v-icon>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title>
            {{item.title}}
          </v-list-item-title>

          <v-list-item-subtitle v-text="item.created_at"></v-list-item-subtitle>
        </v-list-item-content>

        <v-list-item-action>
          <v-btn icon :to="`/articles/detail/${item.id}`">
            <v-icon color="grey lighten-1">mdi-information</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
export default {
  name: 'ArticleList',
  data() {
    return {
      articles: [],
    };
  },
  mounted() {
    this.$axios.get('/articles').then((data) => {
      this.articles = data.data;
    });
  },
};
</script>
