import json
import os

# This is real S4 Physics content (Lenses and Refraction) formatted with metadata
corpus = [
    {
        "subject": "Physics",
        "topic": "Thin Lenses",
        "page": 1,
        "text": "A lens is a transparent medium bounded by two surfaces, at least one of which is curved. A convex lens is thicker in the middle than at the edges and converges light rays. A concave lens is thinner in the middle and diverges light rays. The principal axis is a line passing through the center of the lens perpendicular to its surface. The principal focus (F) is the point where rays parallel to the principal axis converge or appear to diverge from after refraction. The focal length (f) is the distance from the optical center to the principal focus."
    },
    {
        "subject": "Physics",
        "topic": "Thin Lenses",
        "page": 2,
        "text": "Ray diagrams for convex lenses: 1. A ray parallel to the principal axis passes through the principal focus after refraction. 2. A ray passing through the optical center goes straight without deviation. 3. A ray passing through the principal focus emerges parallel to the principal axis. The lens formula is 1/f = 1/v - 1/u, where f is focal length, v is image distance, and u is object distance. The magnification m = v/u = height of image / height of object."
    },
    {
        "subject": "Physics",
        "topic": "Refraction of Light",
        "page": 3,
        "text": "Refraction is the bending of light as it passes from one medium to another. The refractive index (n) of a medium is the ratio of the speed of light in a vacuum (c) to the speed of light in the medium (v): n = c/v. Snell's Law states that n1 * sin(theta1) = n2 * sin(theta2), where theta1 is the angle of incidence and theta2 is the angle of refraction. Total internal reflection occurs when light travels from a denser to a less dense medium and the angle of incidence exceeds the critical angle."
    },
    {
        "subject": "Physics",
        "topic": "Optical Instruments",
        "page": 4,
        "text": "A simple microscope consists of a single convex lens of short focal length. The magnifying power is given by M = 1 + D/f, where D is the least distance of distinct vision (usually 25 cm). A compound microscope uses two convex lenses: the objective and the eyepiece. The objective forms a real, inverted, and magnified image, which acts as an object for the eyepiece. The eyepiece then forms a virtual, magnified image."
    },
        {
        "subject": "Physics",
        "topic": "Thin Lenses",
        "page": 2,
        "text": "The power of a lens (P) is the measure of its ability to converge or diverge light. It is defined as the reciprocal of the focal length (f) measured in meters. The formula is P = 1/f. The SI unit of power is the diopter (D). A convex lens has positive power, while a concave lens has negative power. Imbaraga z'ikirahure (lens power) ibarwa hakoreshejwe formula P = 1/f."
    }
]

# Save to processed folder
os.makedirs("backend/data/processed", exist_ok=True)
with open("backend/data/processed/physics_corpus.json", "w", encoding="utf-8") as f:
    json.dump(corpus, f, indent=4)

print(f"✅ Created corpus with {len(corpus)} pages at backend/data/processed/physics_corpus.json")
