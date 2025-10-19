<script setup>
</script>

<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <!-- Логотип -->
            <router-link class="navbar-brand" to="/">
                🎬 Киносайт
            </router-link>

            <!-- Меню -->
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <router-link class="nav-link" to="/movie/">Фильмы</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Личности</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="/">Жанры</router-link>
                    </li>
                </ul>

                <!-- Правая часть навигации -->
                <ul class="navbar-nav">
                    <!-- Поиск -->
                    <li class="nav-item">
                        <form class="d-flex" action="#" method="get">
                            <input class="form-control2 me-2" type="search" name="q" placeholder="Поиск..." aria-label="Search">
                            <button class="btn btn-outline-light" type="submit">Найти</button>
                        </form>
                    </li>

                    <!-- Личный кабинет / Авторизация -->
                    <li class="nav-item dropdown">
                        <router-link class="nav-link dropdown-toggle" to="#" id="userDropdown" role="button"
                           data-bs-toggle="dropdown" aria-expanded="false">
                            👤 user.username
                        </router-link>
                        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                            <li><router-link class="dropdown-item" to="#">Личный кабинет</router-link></li>
                            <li><router-link class="dropdown-item" to="#">Мои оценки</router-link></li>
                            <li><router-link class="dropdown-item" to="#">Хочу посмотреть</router-link></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><router-link class="dropdown-item" to="/admin/">Админ Панель</router-link></li>
                            <li><router-link class="dropdown-item" to="#">Выйти</router-link></li>
                        </ul>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="#">Войти</router-link>
                    </li>
                    <li class="nav-item">
                        <router-link class="nav-link" to="#">Регистрация</router-link>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <router-view/>
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
</style>