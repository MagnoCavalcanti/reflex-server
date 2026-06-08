from fastapi import APIRouter, Depends, status, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..utils import get_db_session, get_current_user
from ..repositories import CoursesUseCases, UserUseCases, ModuleUseCases
from ..schemas import Course as CourseSchema
from io import BytesIO
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas


def _build_certificate_pdf(certificate: dict) -> bytes:
    buffer = BytesIO()
    page_width, page_height = landscape(A4)
    pdf = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    # Base colors aligned with frontend palette (indigo/blue/gray).
    indigo_dark = colors.HexColor("#1e1b4b")
    indigo = colors.HexColor("#3730a3")
    blue = colors.HexColor("#2563eb")
    blue_light = colors.HexColor("#60a5fa")
    slate = colors.HexColor("#334155")
    slate_light = colors.HexColor("#cbd5e1")
    white = colors.white

    # Background.
    pdf.setFillColor(colors.HexColor("#f8fafc"))
    pdf.rect(0, 0, page_width, page_height, stroke=0, fill=1)

    # Diagonal watermark.
    pdf.saveState()
    pdf.translate(page_width / 2, page_height / 2)
    pdf.rotate(35)
    pdf.setFillColor(colors.HexColor("#e2e8f0"))
    pdf.setFillAlpha(0.3)
    pdf.setFont("Helvetica-Bold", 120)
    pdf.drawCentredString(0, 0, "CERTIFICADO")
    pdf.setFillAlpha(1)
    pdf.restoreState()

    # Double frame.
    margin = 24
    pdf.setStrokeColor(slate_light)
    pdf.setLineWidth(2)
    pdf.rect(margin, margin, page_width - (margin * 2), page_height - (margin * 2), stroke=1, fill=0)
    pdf.setStrokeColor(colors.HexColor("#94a3b8"))
    pdf.setLineWidth(0.8)
    pdf.rect(margin + 10, margin + 10, page_width - (margin * 2) - 20, page_height - (margin * 2) - 20, stroke=1, fill=0)

    # Decorative ribbons and corners.
    pdf.setFillColor(indigo_dark)
    pdf.rect(0, page_height - 70, page_width, 70, stroke=0, fill=1)
    pdf.setFillColor(indigo)
    pdf.rect(0, page_height - 78, page_width * 0.6, 8, stroke=0, fill=1)
    pdf.setFillColor(blue)
    pdf.rect(0, 0, page_width, 36, stroke=0, fill=1)
    pdf.setFillColor(indigo)
    pdf.rect(0, 36, page_width, 10, stroke=0, fill=1)
    pdf.setFillColor(blue_light)
    pdf.rect(page_width * 0.35, 46, page_width * 0.65, 6, stroke=0, fill=1)

    # Corner polygons for premium look.
    pdf.setFillColor(colors.HexColor("#0f172a"))
    top_left = pdf.beginPath()
    top_left.moveTo(0, page_height)
    top_left.lineTo(120, page_height)
    top_left.lineTo(0, page_height - 70)
    top_left.close()
    pdf.drawPath(top_left, stroke=0, fill=1)

    bottom_right = pdf.beginPath()
    bottom_right.moveTo(page_width, 0)
    bottom_right.lineTo(page_width - 130, 0)
    bottom_right.lineTo(page_width, 70)
    bottom_right.close()
    pdf.drawPath(bottom_right, stroke=0, fill=1)

    # Header.
    pdf.setFillColor(white)
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(40, page_height - 42, "Plataforma de Cursos")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(40, page_height - 58, "Certificação de conclusão")
    pdf.setFont("Helvetica-Bold", 34)
    pdf.drawCentredString(page_width / 2, page_height - 122, "CERTIFICADO")

    # Main text.
    student_name = certificate.get("student_name") or "Aluno(a)"
    course_title = certificate.get("course_title") or "Curso"
    professor_name = certificate.get("professor_name") or "Professor não informado"
    issued_at = certificate.get("issued_at") or "-"
    verification_code = certificate.get("verification_code") or "-"
    digital_signature = certificate.get("digital_signature") or "-"

    pdf.setFillColor(slate)
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(page_width / 2, page_height - 175, "Certificamos que")

    pdf.setFont("Times-BoldItalic", 34)
    pdf.setFillColor(indigo_dark)
    pdf.drawCentredString(page_width / 2, page_height - 220, student_name[:60])

    pdf.setFillColor(slate)
    pdf.setFont("Helvetica", 14)
    pdf.drawCentredString(page_width / 2, page_height - 257, "concluiu com êxito o curso")

    pdf.setFillColor(indigo)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(page_width / 2, page_height - 290, course_title[:70])

    # Divider line.
    pdf.setStrokeColor(colors.HexColor("#94a3b8"))
    pdf.setLineWidth(1)
    pdf.line((page_width / 2) - 210, page_height - 304, (page_width / 2) + 210, page_height - 304)

    pdf.setFillColor(slate)
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(page_width / 2, page_height - 324, f"Professor responsável: {professor_name[:60]}")
    pdf.drawCentredString(page_width / 2, page_height - 344, f"Data de emissão: {issued_at}")

    # Left-side seal.
    seal_x = 95
    seal_y = 120
    pdf.setFillColor(colors.HexColor("#dbeafe"))
    pdf.circle(seal_x, seal_y, 42, stroke=0, fill=1)
    pdf.setStrokeColor(indigo)
    pdf.setLineWidth(2)
    pdf.circle(seal_x, seal_y, 42, stroke=1, fill=0)
    pdf.setLineWidth(1)
    pdf.circle(seal_x, seal_y, 34, stroke=1, fill=0)
    pdf.setFillColor(indigo_dark)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawCentredString(seal_x, seal_y + 4, "CURSO")
    pdf.drawCentredString(seal_x, seal_y - 10, "CONCLUÍDO")

    # Signature area.
    signature_y = 110
    line_width = 220
    left_x = (page_width / 2) - 260
    right_x = (page_width / 2) + 40
    pdf.setStrokeColor(colors.HexColor("#64748b"))
    pdf.setLineWidth(1)
    pdf.line(left_x, signature_y, left_x + line_width, signature_y)
    pdf.line(right_x, signature_y, right_x + line_width, signature_y)

    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(colors.HexColor("#475569"))
    pdf.drawCentredString(left_x + (line_width / 2), signature_y - 18, "Diretoria Pedagógica")
    pdf.drawCentredString(right_x + (line_width / 2), signature_y - 18, "Aluno(a)")

    # Footer legend.
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(white)
    pdf.drawRightString(page_width - 32, 28, f"Código de verificação: {verification_code}")
    signature_preview = digital_signature[:18] + "..." + digital_signature[-10:] if len(digital_signature) > 32 else digital_signature
    pdf.drawRightString(page_width - 32, 18, f"Assinatura digital: {signature_preview}")

    pdf.showPage()
    pdf.save()
    return buffer.getvalue()


course_router = APIRouter(prefix="/courses")


@course_router.post("/")
def create_course(
    course_data: CourseSchema,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    course_uc = CoursesUseCases(db)
    user_uc = UserUseCases(db)
    current_user_id = user_uc.user_id_by_username(current_user["sub"])

    if course_data.professor_id != current_user_id:
        raise HTTPException(
            detail="Você só pode criar cursos para o professor autenticado.",
            status_code=status.HTTP_403_FORBIDDEN
        )

    new_course = course_uc.create_course(course_data)
    return JSONResponse(
        content=jsonable_encoder(new_course),
        status_code=status.HTTP_201_CREATED
    )

@course_router.put("/{course_id}")
def update_course(
    course_id: int,
    course_data: CourseSchema,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    course_uc = CoursesUseCases(db)
    user_uc = UserUseCases(db)
    current_user_id = user_uc.user_id_by_username(current_user["sub"])

    if course_data.professor_id != current_user_id:
        raise HTTPException(
            detail="Você só pode atualizar cursos do professor autenticado.",
            status_code=status.HTTP_403_FORBIDDEN
        )

    updated_course = course_uc.update_course(course_id, course_data)
    return JSONResponse(
        content=jsonable_encoder(updated_course),
        status_code=status.HTTP_200_OK
    )

@course_router.post("/enrollments")
def enroll_in_course(course_id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    user_uc = UserUseCases(db)
    user_uc.enroll(current_user["sub"], course_id)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )

@course_router.get("/")
def list_courses(
    search: str | None = Query(default=None),
    area: str | None = Query(default=None),
    level: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    db: Session = Depends(get_db_session)
):
    course_uc = CoursesUseCases(db)
    courses = course_uc.list_courses(
        search=search,
        area=area,
        level=level,
        page=page,
        page_size=page_size
    )
    return JSONResponse(
        content=jsonable_encoder(courses),
        status_code=status.HTTP_200_OK
    )


@course_router.get("/{course_id}")
def get_course_details(course_id: int, db: Session = Depends(get_db_session)):
    course_uc = CoursesUseCases(db)
    course = course_uc.get_course_details(course_id)
    return JSONResponse(
        content=jsonable_encoder(course),
        status_code=status.HTTP_200_OK
    )


@course_router.get("/{course_id}/modules")
def list_course_modules(course_id: int, db: Session = Depends(get_db_session)):
    module_uc = ModuleUseCases(db)
    modules = module_uc.list_by_course_id(course_id)
    return JSONResponse(
        content=jsonable_encoder(modules),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/{course_id}/students")
def list_course_students(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    students = user_uc.list_students_by_course(course_id, current_user["sub"])
    return JSONResponse(
        content=jsonable_encoder(students),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/professor/me/enrollments")
def get_professor_enrollment_metrics(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    professor = user_uc.ensure_professor(current_user["sub"])
    course_uc = CoursesUseCases(db)
    metrics = course_uc.get_professor_course_enrollment_metrics(professor.id)
    return JSONResponse(
        content=jsonable_encoder(metrics),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/{course_id}/quiz-metrics")
def get_course_quiz_metrics(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    professor = user_uc.ensure_professor(current_user["sub"])
    course_uc = CoursesUseCases(db)
    metrics = course_uc.get_course_quiz_question_metrics(course_id, professor.id)
    return JSONResponse(
        content=jsonable_encoder(metrics),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/students/me/progress")
def get_student_progress(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    progress = user_uc.get_student_course_progress(current_user["sub"])
    return JSONResponse(
        content=jsonable_encoder(progress),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/{course_id}/students/me/completed-lessons")
def get_student_completed_lessons_by_course(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    lesson_ids = user_uc.get_completed_lesson_ids_by_course(current_user["sub"], course_id)
    return JSONResponse(
        content=jsonable_encoder({"course_id": course_id, "lesson_ids": lesson_ids}),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/{course_id}/students/me/certificate")
def get_student_course_certificate(
    course_id: int,
    download: bool = Query(default=False),
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    certificate = user_uc.get_course_certificate_payload(current_user["sub"], course_id)

    if not download:
        return JSONResponse(
            content=jsonable_encoder(certificate),
            status_code=status.HTTP_200_OK
        )

    if not certificate["eligible"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Curso ainda não concluído para emissão de certificado"
        )

    safe_course_title = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in certificate["course_title"])
    filename = f"certificado_{safe_course_title}_{course_id}.pdf"
    file_buffer = BytesIO(_build_certificate_pdf(certificate))
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(file_buffer, media_type="application/pdf", headers=headers)
