from flask import Blueprint, request, jsonify
from services.llm_service import initialize_chain, retrieve_relevant_chunks
from services.embedding_service import model
import globals

chat_bp = Blueprint('chat_bp', __name__)

# Initialize LLM Chain
chain = initialize_chain()

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("question", "")

    if not user_input:
        return jsonify({"response": "Please provide a question."})

    try:
        # Check if the index and chunks are initialized
        if not globals.index or not globals.chunks:
            return jsonify({"response": "Please upload a PDF file first."})

        indices = retrieve_relevant_chunks(globals.index, user_input, model)
        context = " \n\n ".join([globals.chunks[i] for i in indices[0]])  # Access the first array of indices

        user_input = f"""
        The user asked: {user_input}
        Based on the following context, provide a helpful answer. Your answer should strictly be within the context:
        {context}
        """
        print("***********************************************************************")
        print("\n")
        print("\n")
        print("\n")
        print("\n")
        print(user_input)
        print("\n")
        print("\n")
        print("\n")
        print("\n")        
        print("***********************************************************************")
        response = chain.run({"question": user_input})
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})
