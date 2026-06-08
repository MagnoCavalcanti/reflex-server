from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from passlib.context import CryptContext
import yt_dlp

from app.core.db_connection import Session
from app.models import (
    User,
    Course,
    Module,
    Lesson,
    LessonVideo,
    LessonQuiz,
    QuizQuestion,
    QuizOption,
    CourseEnrollment,
    LessonCompletion,
    QuizAttempt,
    QuizAnswer,
    ModuleCompletion,
    RefreshToken,
)


crypt_context = CryptContext(schemes=["sha256_crypt"])
DEFAULT_USER_PASSWORD = "12345678"
FIRST_NAMES = [
    "João",
    "Maria",
    "Pedro",
    "Ana",
    "Lucas",
    "Beatriz",
    "Rafael",
    "Carla",
    "Bruno",
    "Juliana",
]
LAST_NAMES = [
    "Silva",
    "Santos",
    "Oliveira",
    "Souza",
    "Costa",
    "Pereira",
    "Rodrigues",
    "Almeida",
    "Nascimento",
    "Lima",
]


COURSE_SOURCES = [
    ("Maratona Java Virado no Jiraya (DevDojo)", "https://www.youtube.com/playlist?list=PL62G310vn6nFIsOCC0H-C2infYgwm8SWW"),
    ("Curso Java Completo (DevDojo)", "https://www.youtube.com/watch?v=kkOSweUhGZM"),
    ("Java do Zero ao Júnior", "https://www.youtube.com/watch?v=SIFkaBzYAyc"),
    ("Curso de Java - Loiane Groner", "https://www.youtube.com/playlist?list=PLEdPHGYHbNwu8nKSmr4bgyy6QZJ8M5cA6"),
    ("Curso de Java POO (Curso em Vídeo)", "https://www.youtube.com/playlist?list=PLHz_AreHm4dkZ9-atkcmcBaMZdmLHft8n"),
    ("Curso de JavaScript (Curso em Vídeo)", "https://www.youtube.com/playlist?list=PLHz_AreHm4dlsK3Nr9GVvXCbpQyHQl1o1"),
    ("JavaScript Moderno Completo", "https://www.youtube.com/results?search_query=javascript+completo+curso"),
    ("HTML5 e CSS3 Módulo 1", "https://www.youtube.com/playlist?list=PLHz_AreHm4dlAnJ_jJtV29RFxnPHDuk9o"),
    ("HTML5 e CSS3 Módulo 2", "https://www.youtube.com/playlist?list=PLHz_AreHm4dlFPrCXCmd5g92860x_Pbr"),
    ("HTML5 e CSS3 Módulo 3", "https://www.youtube.com/playlist?list=PLHz_AreHm4dkZ9-atkcmcBaMZdmLHft8n"),
    ("HTML5 e CSS3 Módulo 4", "https://www.youtube.com/playlist?list=PLHz_AreHm4dmDP_RWdiKekjTEmCuq_MW2"),
    ("Python Mundo 1", "https://www.youtube.com/playlist?list=PLHz_AreHm4dlKP6QQCekuIPky1CiwmdI6"),
    ("Python Mundo 2", "https://www.youtube.com/playlist?list=PLHz_AreHm4dlFNaTQU5e91vg9O7q6S5yC"),
    ("Python Mundo 3", "https://www.youtube.com/playlist?list=PLHz_AreHm4dm6wYOIW20Nyg12TAjmMGT-"),
    ("Jornada Python (Hashtag Programação)", "https://www.youtube.com/playlist?list=PLenUrGUoOG73_Ne6SBs4PV_s4gHpvImFr"),
    ("Python Completo para Iniciantes", "https://www.youtube.com/results?search_query=python+curso+completo"),
    ("Django do Zero", "https://www.youtube.com/results?search_query=django+curso+completo"),
    ("Flask Completo", "https://www.youtube.com/results?search_query=flask+curso+completo"),
    ("React JS Completo", "https://www.youtube.com/results?search_query=react+curso+completo"),
    ("Next.js Completo", "https://www.youtube.com/results?search_query=nextjs+curso+completo"),
    ("Node.js Completo", "https://www.youtube.com/results?search_query=nodejs+curso+completo"),
    ("TypeScript Completo", "https://www.youtube.com/results?search_query=typescript+curso+completo"),
    ("FastAPI Completo", "https://www.youtube.com/results?search_query=fastapi+curso+completo"),
    ("Spring Boot Completo", "https://www.youtube.com/results?search_query=spring+boot+curso+completo"),
    ("C# Completo", "https://www.youtube.com/results?search_query=c%23+curso+completo"),
    ("ASP.NET Core Completo", "https://www.youtube.com/results?search_query=asp.net+core+curso+completo"),
    ("PHP Completo", "https://www.youtube.com/results?search_query=php+curso+completo"),
    ("Laravel Completo", "https://www.youtube.com/results?search_query=laravel+curso+completo"),
    ("Banco de Dados SQL", "https://www.youtube.com/results?search_query=sql+curso+completo"),
    ("PostgreSQL Completo", "https://www.youtube.com/results?search_query=postgresql+curso+completo"),
    ("MySQL Completo", "https://www.youtube.com/results?search_query=mysql+curso+completo"),
    ("MongoDB Completo", "https://www.youtube.com/results?search_query=mongodb+curso+completo"),
    ("Git e GitHub Completo", "https://www.youtube.com/results?search_query=git+github+curso+completo"),
    ("Docker Completo", "https://www.youtube.com/results?search_query=docker+curso+completo"),
    ("Kubernetes Completo", "https://www.youtube.com/results?search_query=kubernetes+curso+completo"),
    ("Linux para Programadores", "https://www.youtube.com/results?search_query=linux+curso+completo"),
    ("Estrutura de Dados", "https://www.youtube.com/results?search_query=estrutura+de+dados+curso+completo"),
    ("Algoritmos e Lógica de Programação", "https://www.youtube.com/results?search_query=algoritmos+e+logica+de+programacao+curso+completo"),
    ("Programação Orientada a Objetos", "https://www.youtube.com/results?search_query=poo+curso+completo"),
    ("Clean Architecture e SOLID", "https://www.youtube.com/results?search_query=clean+architecture+solid+curso+completo"),
]


def infer_area_and_level(title: str, idx: int) -> tuple[str, str]:
    title_lower = title.lower()
    if "java" in title_lower or "spring" in title_lower:
        return "Back-end", "Intermediário"
    if any(word in title_lower for word in ["python", "django", "flask", "fastapi"]):
        return "Back-end", "Iniciante"
    if any(word in title_lower for word in ["html", "css", "javascript", "react", "next", "typescript"]):
        return "Front-end", "Iniciante"
    if any(word in title_lower for word in ["sql", "postgresql", "mysql", "mongodb", "banco"]):
        return "Dados", "Intermediário"
    if any(word in title_lower for word in ["docker", "kubernetes", "linux"]):
        return "DevOps", "Intermediário"
    if any(word in title_lower for word in ["git", "github", "algoritmos", "estrutura", "poo", "clean"]):
        return "Fundamentos", "Iniciante"
    return ("Back-end" if idx % 2 == 0 else "Front-end", "Intermediário")


def build_full_name(index: int, offset: int = 0) -> str:
    first_name = FIRST_NAMES[(index + offset) % len(FIRST_NAMES)]
    last_name = LAST_NAMES[(index * 2 + offset) % len(LAST_NAMES)]
    return f"{first_name} {last_name}"


def extract_public_playlist_videos(url: str) -> list[dict]:
    """
    Retorna vídeos da playlist pública.
    Se não for playlist pública acessível, retorna lista vazia.
    """
    if "playlist?list=" not in url:
        return []

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True,
        "ignoreerrors": True,
        "noplaylist": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
    except Exception:
        return []

    if not info:
        return []

    entries = info.get("entries") or []
    videos: list[dict] = []
    for entry in entries:
        if not entry:
            continue
        video_id = entry.get("id")
        title = (entry.get("title") or "").strip()
        if not video_id:
            continue
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append(
            {
                "id": video_id,
                "title": title if title else f"Vídeo {len(videos) + 1}",
                "url": video_url,
            }
        )
    return videos


def clean_database(session):
    # Delete in dependency order to avoid FK issues.
    for model in [
        QuizAnswer,
        QuizAttempt,
        QuizOption,
        QuizQuestion,
        LessonQuiz,
        LessonVideo,
        LessonCompletion,
        ModuleCompletion,
        Lesson,
        Module,
        CourseEnrollment,
        Course,
        RefreshToken,
        User,
    ]:
        session.query(model).delete()
    session.commit()


def create_users(session) -> tuple[list[User], list[User]]:
    professors: list[User] = []
    students: list[User] = []

    for i in range(1, 9):
        full_name = build_full_name(i - 1, offset=1)
        user = User(
            username=f"prof{i}",
            # Mesma senha para todos os usuários, facilitando login em ambiente de seed.
            password=crypt_context.hash(DEFAULT_USER_PASSWORD),
            email=f"prof{i}@seed.local",
            fullname=full_name,
            telephone=f"(11) 9{i:04d}-{i:04d}",
            type_user="P",
        )
        session.add(user)
        professors.append(user)

    for i in range(1, 21):
        full_name = build_full_name(i - 1, offset=5)
        user = User(
            username=f"aluno{i}",
            # Mesma senha para todos os usuários, facilitando login em ambiente de seed.
            password=crypt_context.hash(DEFAULT_USER_PASSWORD),
            email=f"aluno{i}@seed.local",
            fullname=full_name,
            telephone=f"(21) 9{i:04d}-{(i + 1000):04d}",
            type_user="A",
        )
        session.add(user)
        students.append(user)

    session.commit()
    for u in professors + students:
        session.refresh(u)
    return professors, students


def create_courses_and_content(session, professors: list[User], students: list[User]):
    now = datetime.now(timezone.utc)
    course_counter = 0
    skipped_courses = 0
    global_lesson_index = 0

    for idx, (title, source_url) in enumerate(COURSE_SOURCES, start=1):
        playlist_videos = extract_public_playlist_videos(source_url)
        if not playlist_videos:
            skipped_courses += 1
            print(f"[SKIP] Curso ignorado (playlist não pública/inválida): {title}")
            continue

        area, level = infer_area_and_level(title, idx)
        professor = professors[(idx - 1) % len(professors)]
        course = Course(
            title=title,
            description=(
                f"Curso completo sobre {title}. Conteúdo estruturado com teoria, prática e exercícios.\n"
                f"Playlist/fonte principal: {source_url}"
            ),
            area=area,
            level=level,
            cover_image_url=f"https://picsum.photos/seed/curso-{idx}/900/400",
            status="publicado",
            professor_id=professor.id,
            created_at=now,
            updated_at=now,
        )
        session.add(course)
        session.commit()
        session.refresh(course)
        course_counter += 1

        total_videos = len(playlist_videos)
        total_modules = 3 if total_videos >= 9 else 2 if total_videos >= 4 else 1
        modules: list[Module] = []
        for module_idx in range(1, total_modules + 1):
            module = Module(
                title=f"Módulo {module_idx} - {title}",
                course_id=course.id,
                order_index=module_idx - 1,
            )
            session.add(module)
            modules.append(module)
        session.commit()
        for module in modules:
            session.refresh(module)

        created_lessons: list[Lesson] = []
        video_url_by_lesson_title: dict[str, str] = {}
        for video_idx, video in enumerate(playlist_videos, start=1):
            module = modules[(video_idx - 1) % len(modules)]
            # Define exatamente 20% das aulas como quiz no conjunto total:
            # a cada 5 aulas criadas, 1 vira exercício.
            is_quiz_lesson = (global_lesson_index % 5 == 0)
            content_type = "Q" if is_quiz_lesson else "V"
            lesson_title = f"Aula {video_idx} - {video['title']}"
            lesson = Lesson(
                title=lesson_title,
                content_type=content_type,
                module_id=module.id,
            )
            session.add(lesson)
            created_lessons.append(lesson)
            video_url_by_lesson_title[lesson_title] = video["url"]
            global_lesson_index += 1
        session.commit()
        for lesson in created_lessons:
            session.refresh(lesson)

        for lesson in created_lessons:
            video = LessonVideo(
                lesson_id=lesson.id,
                video_url=video_url_by_lesson_title.get(lesson.title, source_url),
            )
            session.add(video)

            if lesson.content_type == "Q":
                quiz = LessonQuiz(lesson_id=lesson.id)
                session.add(quiz)
                session.commit()
                session.refresh(quiz)

                for q_idx in range(1, 3):
                    question = QuizQuestion(
                        quiz_id=quiz.id,
                        question_text=f"Questão {q_idx} da {lesson.title}",
                    )
                    session.add(question)
                    session.commit()
                    session.refresh(question)

                    for o_idx in range(1, 5):
                        option = QuizOption(
                            question_id=question.id,
                            option_text=f"Opção {o_idx} - Questão {q_idx}",
                            is_correct=(o_idx == 1),
                        )
                        session.add(option)
        session.commit()

        # Enroll students (10 per course).
        enrolled_students = students[(idx - 1) % len(students):] + students[: (idx - 1) % len(students)]
        enrolled_students = enrolled_students[:10]
        for student in enrolled_students:
            enrollment = CourseEnrollment(
                user_id=student.id,
                course_id=course.id,
                registration_date=date.today(),
            )
            session.add(enrollment)
        session.commit()

        # Mark first 2 lessons as completed for first 3 enrolled students to simulate progress.
        first_lessons = created_lessons[:2]
        for student in enrolled_students[:3]:
            for lesson in first_lessons:
                completion = LessonCompletion(
                    user_id=student.id,
                    lesson_id=lesson.id,
                    completion_date=date.today(),
                )
                session.add(completion)
        session.commit()

    return course_counter, skipped_courses


def main():
    session = Session()
    try:
        clean_database(session)
        professors, students = create_users(session)
        courses_total, skipped_courses = create_courses_and_content(session, professors, students)
        print("Superpopulação concluída com sucesso.")
        print(f"- Senha padrão para todos os usuários: {DEFAULT_USER_PASSWORD}")
        print(f"- Professores criados: {len(professors)}")
        print(f"- Alunos criados: {len(students)}")
        print(f"- Cursos criados: {courses_total}")
        print(f"- Cursos ignorados (playlist não pública/inválida): {skipped_courses}")
    finally:
        session.close()


if __name__ == "__main__":
    main()

