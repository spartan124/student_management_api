"""first migration

Revision ID: 093f0521d6c0
Revises: 
Create Date: 2023-03-23 13:46:14.166661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '093f0521d6c0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('admin_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('admin_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('students',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('student_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('teachers',
    sa.Column('teacher_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('teacher_id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('courses',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_title', sa.String(length=100), nullable=False),
    sa.Column('course_code', sa.String(length=20), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=True),
    sa.Column('credit_unit', sa.Integer(), nullable=False),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['teachers.teacher_id'], ),
    sa.PrimaryKeyConstraint('course_id'),
    sa.UniqueConstraint('course_code')
    )
    op.create_table('student_course',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(), nullable=True),
    sa.Column('gpa', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_id')
    )
    op.create_table('student_results',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('course_code', sa.String(), nullable=False),
    sa.Column('course_title', sa.String(), nullable=False),
    sa.Column('credit_unit', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(length=2), nullable=False),
    sa.Column('earned_credit', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_results')
    op.drop_table('student_course')
    op.drop_table('courses')
    op.drop_table('teachers')
    op.drop_table('students')
    op.drop_table('admins')
    # ### end Alembic commands ###
