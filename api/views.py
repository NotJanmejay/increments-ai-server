from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer, LoginSerializer, PDFEmbeddingSerializer  # Ensure you have a TeacherSerializer, LoginSerializer
from django.contrib.auth.hashers import check_password
from rest_framework.parsers import MultiPartParser, FormParser
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from django.core.files.storage import default_storage
import os
import random
import string
from dotenv import load_dotenv

load_dotenv()

def generate_random_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))
# Student Views
@api_view(["POST"])
def create_student(request):
    """Create a new student and return the generated password."""
    if request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            # Generate a new random password
            random_password = generate_random_password()

            # Assign the generated password to the serializer's data
            serializer.validated_data['password'] = random_password

            # Save the student instance
            student = serializer.save()

            return Response(
                {
                    "message": "Student information saved successfully!",
                    "generated_password": random_password,  # Return this for future login
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_students(request):
    """Retrieve all student records."""
    if request.method == "GET":
        students = Student.objects.all()  # Retrieve all student records
        serializer = StudentSerializer(students, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data


@api_view(["POST"])
def login_student(request):
    """Authenticate student and return student data if credentials match."""
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            # Get the student instance by email
            student = Student.objects.get(email=email)

            # Check if the provided password matches the hashed password
            if check_password(password, student.password):
                student_data = {
                    "name": student.name,
                    "email": student.email,
                    "standard": student.standard,
                    "contact_number": student.contact_number,
                    "parent_email": student.parent_email,
                }
                return Response(
                    {"message": "Login successful!", "student_data": student_data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"message": "Invalid password."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Student.DoesNotExist:
            return Response(
                {"message": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Teacher Views

@api_view(["POST"])
def create_teacher(request):
    serializer = TeacherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Teacher information saved successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_teachers(request):
    teachers = Teacher.objects.all()
    serializer = TeacherSerializer(teachers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_teacher(request, name):
    try:
        teacher = Teacher.objects.get(name=name)  # Adjust based on your primary key
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Teacher.DoesNotExist:
        return Response({"error": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)




# PDF Embeddings

os.environ["REQUESTS_CA_BUNDLE"] = (
    "./certificate.cer"  # To Bypass Self Signed Certificate Error
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser])
def upload_pdf(request):
    """Upload a PDF file, create embeddings, and store them in Pinecone."""
    pdf_file = request.FILES.get('file')  # Ensure the key matches your request

    if not pdf_file:
        return Response({"error": "PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Save the uploaded file temporarily
    file_path = default_storage.save(pdf_file.name, pdf_file)

    # Load and read the PDF document using the file path
    file_loader = PyPDFLoader(file_path)  # Pass the file path to PyPDFLoader
    docs = file_loader.load()

    # Chunk the document into smaller parts
    chunk_size = 800
    overlap_size = 50
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap_size)
    chunked_data = text_splitter.split_documents(docs)

    # Initialize OpenAI embeddings and Pinecone
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
    pc = Pinecone(api_key=PINECONE_API_KEY, ssl_verify=False)
    index = pc.Index("increments")  # Your Pinecone index name

    vector_store = PineconeVectorStore(index=index, embedding=embeddings)

    # Add embeddings to Pinecone
    for i, doc in enumerate(chunked_data):
        doc_id = f"doc_{i}"  # Create a unique ID for each chunk
        vector_store.add_documents(documents=[doc], ids=[doc_id])

    # Optionally, delete the file after processing if you don't need to keep it
    os.remove(file_path)

    return Response({"message": "PDF uploaded and embeddings stored successfully!"}, status=status.HTTP_201_CREATED)