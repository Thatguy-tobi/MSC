from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        try:
            mag_sz = float(request.form.get('mag_sz'))
            img_sz = float(request.form.get('img_sz'))
            img_ut = request.form.get('img_ut').strip().lower()
            real_ut = request.form.get('real_ut').strip().lower()

            if mag_sz == 0:
                return render_template('index.html', error="Magnification cannot be zero.")

            # Convert input to mm
            size_in_mm = 0.0
            if img_ut == "cm": size_in_mm = img_sz * 10
            elif img_ut == "mm": size_in_mm = img_sz
            elif img_ut == "um": size_in_mm = img_sz / 1000
            elif img_ut == "nm": size_in_mm = img_sz / 1000000

            # Calculate real size in mm
            real_size_mm = size_in_mm / mag_sz

            # Convert to required output unit
            final_size = 0.0
            if real_ut == "cm": final_size = real_size_mm / 10
            elif real_ut == "mm": final_size = real_size_mm
            elif real_ut == "um": final_size = real_size_mm * 1000
            elif real_ut == "nm": final_size = real_size_mm * 1000000

            result = f"{final_size:g} {real_ut}"
        except ValueError:
            error = "Please enter valid numeric values."

    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Running on port 5001 to avoid conflicts