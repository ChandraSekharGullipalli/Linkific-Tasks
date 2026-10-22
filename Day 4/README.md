# Day 4 – NumPy Operations and Patterns

## 1. Objective
Practice NumPy array manipulation, statistical analysis, and performance comparison using Python.

## 2. Tools Used
- Python 3.13
- NumPy
- Jupyter Notebook
- Visual Studio Code

## 3. Topics Covered

### Array Manipulation
- Creating NumPy arrays
- Array indexing and slicing
- Reshaping and flattening
- Appending, inserting, and deleting elements
- Combining and splitting arrays
- Sorting and filtering arrays
- Finding unique values
- Copying arrays

### Statistical Analysis
- Sum and mean
- Median
- Minimum and maximum
- Variance
- Standard deviation
- Employee salary analysis

### Performance Comparison
- Python loops
- NumPy vectorization
- Measuring execution time
- Comparing performance on different dataset sizes

## 4. NumPy Patterns

### Pattern 1: Array Creation
```python
import numpy as np

arr = np.array([10, 20, 30, 40])
print(arr)
```

### Pattern 2: Filtering
```python
arr = np.array([10, 20, 30, 40, 50])
print(arr[arr > 25])
```

### Pattern 3: Reshaping
```python
arr = np.arange(1, 7)
print(arr.reshape(2, 3))
```

### Pattern 4: Statistical Analysis
```python
arr = np.array([10, 20, 30, 40, 50])

print("Mean:", np.mean(arr))
print("Maximum:", np.max(arr))
print("Minimum:", np.min(arr))
```

### Pattern 5: Vectorization
```python
arr = np.array([1, 2, 3, 4, 5])
result = arr * 2

print(result)
```

## 5. How to Run
1. Install Python.
2. Install NumPy using `python -m pip install numpy`.
3. Open `numpy_operations.ipynb` in VS Code.
4. Select the Python kernel.
5. Run the notebook cells and review the outputs.

## 6. Learning Outcomes
- Learned common NumPy array manipulation techniques.
- Practiced statistical calculations.
- Used Boolean conditions to filter data.
- Compared Python loops with NumPy vectorization.
- Understood how NumPy supports efficient numerical data processing.

## 7. Conclusion
This practice helped develop fundamental NumPy skills useful for data analysis, data processing, and future data engineering tasks.