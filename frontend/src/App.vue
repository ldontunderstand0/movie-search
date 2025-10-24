<script setup>
import { watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const auth = useAuthStore()

watch(() => route.fullPath, async() => {
  await auth.fetchUser()
},
{ immediate: true }
)

</script>

<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <!-- Логотип -->
            

            <!-- Меню -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <router-link class="navbar-brand" to="/">
                Киносайт
                </router-link>
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{name: 'movie'}">Фильмы</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{name: 'person'}">Личности</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{name: 'genre'}">Жанры</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" :to="{name: 'country'}">Страны</router-link>
                    </li>
                </ul>

                <!-- Правая часть навигации -->
                <ul class="navbar-nav">
                    <!-- Поиск -->
                    <!-- <li class="nav-item">
                        <form class="d-flex" action="#" method="get">
                            <input class="form-control2 me-2" type="search" name="q" placeholder="Поиск..." aria-label="Search">
                            <button class="btn btn-outline-light" type="submit">Найти</button>
                        </form>
                    </li> -->

                    <!-- Личный кабинет / Авторизация -->
                    <li class="nav-item dropdown">
                        <router-link v-if="auth.user" class="nav-link dropdown-toggle" id="userDropdown" role="button"
                           data-bs-toggle="dropdown" aria-expanded="false">
                            👤 {{ auth.user.username }}
                        </router-link>
                        <ul v-if="auth.user" class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                            <li><router-link class="dropdown-item" :to="{name: 'user-detail', params: {id: auth.user.id} }">Личный кабинет</router-link></li>
                            <li><router-link class="dropdown-item" :to="{name: 'rating', query: {user: auth.user.id}}">Мои оценки</router-link></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><router-link v-if="auth.user.is_staff" class="dropdown-item" to="/admin">Админ Панель</router-link></li>
                            <li><router-link class="dropdown-item" :to="{name: 'logout'}">Выйти</router-link></li>
                        </ul>
                    </li>
                    <li v-if="!auth.user" class="nav-item">
                        <router-link  class="nav-link" :to="{name: 'login'}">Войти</router-link>
                    </li>
                    <li v-if="!auth.user" class="nav-item">
                        <router-link class="nav-link" to="#">Регистрация</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <router-view :key="$route.fullPath"/>
  </div>
</template>

<style>
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 0;
    color: #333;
}
  html, body {
  height: auto !important;
  overflow-y: auto !important;
}
/* Сброс стилей Bootstrap */
.navbar {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background: #1a1a1a;
    border-bottom: 3px solid #ff8a00;
    padding: 0;
    margin: 0;
}

.navbar .container {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
}

/* Логотип */
.navbar-brand {
    font-size: 24px;
    font-weight: bold;
    color: #ff8a00 !important;
    text-decoration: none;
    padding: 15px 0;
    margin-right: 40px;
}

/* Основная навигация */
.navbar-collapse {
    display: flex;
    flex-grow: 1;
    justify-content: space-between;
}

.navbar-nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    align-items: center;
}

.navbar-nav.me-auto {
    margin-right: auto;
}

.nav-item {
    margin: 0 5px;
}

.nav-link {
    color: #ffffff !important;
    text-decoration: none;
    padding: 15px 20px;
    display: block;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.nav-link:hover {
    background: rgba(255, 138, 0, 0.1);
    color: #ff8a00 !important;
}

/* Правая часть навигации */
.navbar-nav:not(.me-auto) {
    display: flex;
    align-items: center;
    gap: 15px;
}

/* Форма поиска */
.d-flex {
    display: flex;
    gap: 10px;
    align-items: center;
}

.form-control2 {
    padding: 8px 15px;
    border: 1px solid #444;
    border-radius: 20px;
    background: #2d2d2d;
    color: white;
    min-width: 250px;
}

.form-control2::placeholder {
    color: #888;
}

.btn-outline-light {
    padding: 8px 20px;
    border: 1px solid #666;
    border-radius: 20px;
    background: transparent;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-outline-light:hover {
    background: #ff8a00;
    border-color: #ff8a00;
}

/* Выпадающее меню */
.dropdown {
    position: relative;
}

.dropdown-toggle {
    display: flex;
    align-items: center;
    gap: 5px;
}

.dropdown-menu {
    position: absolute;
    right: 0;
    top: 100%;
    background: #2d2d2d;
    border: 1px solid #444;
    border-radius: 4px;
    min-width: 200px;
    display: none;
    z-index: 1000;
}

.dropdown:hover .dropdown-menu {
    display: block;
}

.dropdown-item {
    display: block;
    padding: 10px 15px;
    color: white;
    text-decoration: none;
    transition: background 0.3s ease;
}

.dropdown-item:hover {
    background: #ff8a00;
}

@media (max-width: 1024px) {
  .navbar .container {
    padding: 0 15px;
  }

  .navbar-brand {
    font-size: 22px;
    margin-right: 20px;
  }

  .nav-link {
    padding: 12px 16px;
  }

  .form-control2 {
    min-width: 180px;
  }
}

/* --- Мобильные устройства (до 768px) --- */
@media (max-width: 768px) {
    .nav-item {
        margin-top: 1%;
    }
  .navbar {
    flex-direction: column;
    align-items: flex-start;
  }

  .navbar .container {
    flex-direction: column;
    align-items: flex-start;
  }

  /* Основное меню */
  .navbar-collapse {
    align-items: flex-start;
    width: 100%;
  }

  .navbar-nav {
    width: 100%;
    margin-top: 5px;
  }

  .navbar-nav.me-auto {
    margin-right: 0;
  }

  .nav-item {
    width: 100%;
  }

  .nav-link {
    width: 100%;
    padding: 10px 15px;
    text-align: left;
  }


  /* Правая часть */
  .navbar-nav:not(.me-auto) {
    align-items: flex-start;
    width: 100%;
    gap: 8px;
  }

  .dropdown-menu {
    display: none;
    width: 100%;
    background: #222;
    border: none;
    margin-top: 5px;
  }

  .dropdown-item {
    padding: 10px;
    font-size: 0.95rem;
  }

  /* Поиск (если включишь обратно) */
  .d-flex {
    width: 100%;
  }

  .form-control2 {
    flex-grow: 1;
    min-width: unset;
  }

  .btn-outline-light {
    padding: 8px 15px;
  }
}
@media (max-width: 640px) {
    .navbar-brand {
    font-size: 18px;
  }
      .nav-link {
    font-size: 13px;
  }
}
/* --- Маленькие телефоны (до 480px) --- */
@media (max-width: 480px) {
  .navbar-collapse {
    flex-direction: column;
    align-items: center;
  }
.navbar-nav:not(.me-auto) {
    max-width: 28%;
  }
  .navbar-brand {
    margin: 0;
  }


  .nav-link {
    font-size: 0.9rem;
    padding: 8px 12px;
  }

  .dropdown-item {
    font-size: 0.9rem;
  }

  .form-control2 {
    padding: 6px 10px;
  }

  .btn-outline-light {
    font-size: 0.9rem;
    padding: 6px 12px;
  }
}

/* --- Очень маленькие экраны (до 360px) --- */
@media (max-width: 360px) {
  .navbar-brand {
    font-size: 18px;
  }

  .nav-link {
    font-size: 0.85rem;
  }

  .dropdown-item {
    font-size: 0.85rem;
  }
}
</style>