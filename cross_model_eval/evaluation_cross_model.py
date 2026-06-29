"""
Cross-Modal Performance Evaluation Lab
Course: Evaluate and Apply Ethical AI Models
Module 1: Cross-modal performance evaluation - Foundation

This lab implements industry-standard metrics for evaluating multimodal AI systems,
focusing on FID scores, CLIP similarity, and Recall@K measurements used in 
enterprise ML workflows for model selection and performance comparison.
"""

import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from scipy.linalg import sqrtm

import warnings
warnings.filterwarnings('ignore')


# PROVIDED CODE - DO NOT MODIFY
def load_sample_data():
    """Load sample multimodal evaluation dataset"""
    np.random.seed(42)

    # Simulate real and generated feature embeddings (768-dimensional)
    real_features = np.random.randn(100, 768)
    generated_features = (
        np.random.randn(100, 768)
        + 0.1 * np.random.randn(100, 768)
    )

    # Simulate image and text embeddings for CLIP evaluation
    image_embeddings = np.random.randn(50, 512)
    text_embeddings = np.random.randn(50, 512)

    # Create some correlated pairs for realistic evaluation
    for i in range(20):
        text_embeddings[i] = (
            image_embeddings[i]
            + 0.2 * np.random.randn(512)
        )

    return (
        real_features,
        generated_features,
        image_embeddings,
        text_embeddings
    )


def visualize_results(fid_score, clip_scores, recall_results):
    """Visualize evaluation results - PROVIDED CODE"""
    fig, (ax1, ax2, ax3) = plt.subplots(
        1,
        3,
        figsize=(15, 4)
    )

    # FID Score
    ax1.bar(
        ['FID Score'],
        [fid_score],
        color='skyblue'
    )
    ax1.set_ylabel('FID Score')
    ax1.set_title('FID Score (Lower is Better)')

    # CLIP Similarities
    ax2.hist(
        clip_scores,
        bins=20,
        alpha=0.7,
        color='lightgreen'
    )
    ax2.set_xlabel('CLIP Similarity Score')
    ax2.set_ylabel('Frequency')
    ax2.set_title('CLIP Similarity Distribution')

    # Recall@K
    k_values = list(recall_results.keys())
    recall_values = list(recall_results.values())

    ax3.plot(
        k_values,
        recall_values,
        'o-',
        color='orange',
        linewidth=2
    )
    ax3.set_xlabel('K Value')
    ax3.set_ylabel('Recall@K')
    ax3.set_title('Recall@K Performance')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


# ================================================================
# YOUR IMPLEMENTATION STARTS HERE
# ================================================================

### PRACTICE CHALLENGE 1 ###
# TASK: Complete the calculate_fid_score() function to compute Fréchet Inception Distance 
# between real and generated features. FID measures the distance between two multivariate 
# Gaussians fitted to feature representations.
# YOUR CODE HERE

def calculate_fid_score(real_features, generated_features):
    """
    Calculate Fréchet Inception Distance between real and generated features.

    Args:
        real_features: numpy array of shape (n_samples, n_features)
        generated_features: numpy array of shape (n_samples, n_features)

    Returns:
        float: FID score (lower is better)
    """
    # TODO: Calculate mean vectors for both distributions
    mu1 = np.mean(real_features, axis=0)
    mu2 = np.mean(generated_features, axis=0)

    # TODO: Calculate covariance matrices for both distributions
    C1 = np.cov(real_features, rowvar=False)
    C2 = np.cov(generated_features, rowvar=False)
    # TODO: Calculate Fréchet distance using the formula:
    # FID = ||mu1 - mu2||^2 + Tr(C1 + C2 - 2*sqrt(C1*C2))

    covmean = sqrtm(C1 @ C2)

    if np.iscomplexobj(covmean):
        covmean = covmean.real

    diff = mu1 - mu2

    fid = diff @ diff + np.trace(C1 + C2 - 2 * covmean)

    return float(np.real(fid))


### PRACTICE CHALLENGE 2 ###
# TASK: Implement calculate_clip_similarity() to measure semantic alignment between 
# image-text pairs using cosine similarity of normalized embeddings.
# YOUR CODE HERE

def calculate_clip_similarity(image_embeddings, text_embeddings):
    """
    Calculate CLIP-style similarity scores between image and text embeddings.

    Args:
        image_embeddings: numpy array of shape (n_samples, embedding_dim)
        text_embeddings: numpy array of shape (n_samples, embedding_dim)

    Returns:
        numpy array: similarity scores between corresponding pairs
    """
    # TODO: Normalize embeddings to unit vectors
    normalized_images = normalize(image_embeddings)
    normalized_texts = normalize(text_embeddings)

    # TODO: Calculate cosine similarity between corresponding pairs
    similarity_matrix = cosine_similarity(
        normalized_images,
        normalized_texts
    )
    # TODO: Return diagonal elements (pair-wise similarities)
    clip_scores = np.diag(similarity_matrix)

    return clip_scores
    


### PRACTICE CHALLENGE 3 ###
# TASK: Complete calculate_recall_at_k() to measure retrieval performance for different K values.
# Recall@K measures how often the correct item appears in top-K retrieved results.
# YOUR CODE HERE

def calculate_recall_at_k(
    image_embeddings,
    text_embeddings,
    k_values=[1, 5, 10]
):
    """
    Calculate Recall@K for image-text retrieval task.

    Args:
        image_embeddings: numpy array of shape (n_samples, embedding_dim)
        text_embeddings: numpy array of shape (n_samples, embedding_dim)  
        k_values: list of K values to evaluate

    Returns:
        dict: recall scores for each K value
    """
    # TODO: Normalize embeddings
    normalized_images = normalize(image_embeddings)
    normalized_texts = normalize(text_embeddings)

    # TODO: Calculate similarity matrix between all image-text pairs
    similarity_matrix = cosine_similarity(normalized_texts, normalized_images)

    # TODO: For each text query, find top-K most similar images

    # TODO: Calculate recall for each K value

    recall_results = {}

    for k in k_values:
        correct = 0

        for i in range(len(text_embeddings)):
            top_k_indices = np.argsort(similarity_matrix[i])[-k:]

            if i in top_k_indices:
                correct += 1
        recall_results[k] = correct / len(text_embeddings)

    return recall_results


# ================================================================
# MAIN EXECUTION AND TESTING
# ================================================================

def main():
    """Main function to test all implemented evaluation metrics"""
    print("🔄 Loading sample multimodal data...")
    (
        real_features,
        generated_features,
        image_embeddings,
        text_embeddings
    ) = load_sample_data()

    print("📊 Running Cross-Modal Performance Evaluation...")
    print("=" * 50)

    # Test FID Score Calculation
    print("1️⃣ Testing FID Score Calculation...")
    fid_score = calculate_fid_score(
        real_features,
        generated_features
    )
    print(f"   FID Score: {fid_score:.4f}")

    # Test CLIP Similarity
    print("\n2️⃣ Testing CLIP Similarity Calculation...")
    clip_scores = calculate_clip_similarity(
        image_embeddings,
        text_embeddings
    )
    print(f"   Average CLIP Similarity: {np.mean(clip_scores):.4f}")
    print(
        f"   Similarity Range: "
        f"[{np.min(clip_scores):.4f}, {np.max(clip_scores):.4f}]"
    )

    # Test Recall@K
    print("\n3️⃣ Testing Recall@K Calculation...")
    recall_results = calculate_recall_at_k(
        image_embeddings,
        text_embeddings
    )
    for k, recall in recall_results.items():
        print(f"   Recall@{k}: {recall:.4f}")

    print("\n📈 Generating visualization...")
    visualize_results(
        fid_score,
        clip_scores,
        recall_results
    )

    print("\n✅ Evaluation Complete!")
    print("💡 Lower FID scores indicate better generation quality")
    print("💡 Higher CLIP similarities indicate better semantic alignment")
    print("💡 Higher Recall@K values indicate better retrieval performance")


if __name__ == "__main__":
    main()
