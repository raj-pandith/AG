with open('index.html', encoding='utf-8') as f:
    content = f.read()

old_block = '<iframe\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tsrc="https://app.edumerge.com/V2/onlineadmissionform/JPS_Enquiry_Form_Web.html?qr=R3lpU3lrWjZSaVl0aDB0Z01QV2NEZz09"\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tstyle="height:810px;width:100%;"></iframe>\n\t\t\t\t\t\t\t\t\t\t\t\t\t</div>'

new_form = '''<form class="admission-form" action="#" method="POST" style="height:810px;width:100%;overflow-y:auto;padding:30px;background:#ffffff;border-radius:8px;box-shadow:0 2px 15px rgba(0,0,0,0.08);font-family:'Open Sans',Arial,sans-serif;box-sizing:border-box;">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div style="max-width:700px;margin:0 auto;">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<h3 style="text-align:center;color:#f98400;margin-bottom:5px;font-size:26px;">LOREM IPSUM ENQUIRY</h3>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<p style="text-align:center;color:#666;margin-bottom:25px;font-size:14px;">Lorem ipsum dolor sit amet consectetur adipiscing elit</p>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div style="display:grid;grid-template-columns:1fr 1fr;gap:15px 20px;">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Student Name <span style="color:red;">*</span></label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<input type="text" name="student_name" required placeholder="Lorem ipsum" style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;box-sizing:border-box;transition:border-color 0.3s;" onfocus="this.style.borderColor='#f98400'" onblur="this.style.borderColor='#ddd'">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Parent/Guardian Name <span style="color:red;">*</span></label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<input type="text" name="parent_name" required placeholder="Dolor sit amet" style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;box-sizing:border-box;transition:border-color 0.3s;" onfocus="this.style.borderColor='#f98400'" onblur="this.style.borderColor='#ddd'">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Email Address <span style="color:red;">*</span></label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<input type="email" name="email" required placeholder="consectetur@example.com" style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;box-sizing:border-box;transition:border-color 0.3s;" onfocus="this.style.borderColor='#f98400'" onblur="this.style.borderColor='#ddd'">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Phone Number <span style="color:red;">*</span></label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<input type="tel" name="phone" required placeholder="+91 99999 99999" pattern="[+]?[0-9\s-]{10,15}" style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;box-sizing:border-box;transition:border-color 0.3s;" onfocus="this.style.borderColor='#f98400'" onblur="this.style.borderColor='#ddd'">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Grade Applying For <span style="color:red;">*</span></label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<select name="grade" required style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;box-sizing:border-box;background:white;transition:border-color 0.3s;" onfocus="this.style.borderColor='#f98400'" onblur="this.style.borderColor='#ddd'">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="">Select Grade</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Pre-School">Pre-School</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Kindergarten">Kindergarten</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 1">Grade 1</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 2">Grade 2</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 3">Grade 3</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 4">Grade 4</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 5">Grade 5</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 6">Grade 6</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 7">Grade 7</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 8">Grade 8</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<option value="Grade 9">Grade 9</option>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</select>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Academic Year</label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<input type="text" name="academic_year" value="2026-27" readonly style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;background:#f9f9f9;color:#666;box-sizing:border-box;">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div style="margin-top:15px;">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<label style="display:block;font-weight:600;color:#333;margin-bottom:5px;font-size:13px;">Message / Query (Optional)</label>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<textarea name="message" rows="3" placeholder="Adipiscing elit sed do eiusmod tempor..." style="width:100%;padding:10px 12px;border:1px solid #ddd;border-radius:4px;font-size:14px;box-sizing:border-box;resize:vertical;transition:border-color 0.3s;font-family:'Open Sans',Arial,sans-serif;" onfocus="this.style.borderColor='#f98400'" onblur="this.style.borderColor='#ddd'"></textarea>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<div style="margin-top:20px;text-align:center;">
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<button type="submit" style="background:linear-gradient(135deg,#f98400,#e67300);color:#fff;border:none;padding:14px 50px;font-size:16px;font-weight:700;border-radius:5px;cursor:pointer;text-transform:uppercase;letter-spacing:0.5px;transition:all 0.3s;box-shadow:0 4px 15px rgba(249,132,0,0.3);" onmouseover="this.style.background='linear-gradient(135deg,#e67300,#d46200)';this.style.transform='translateY(-2px)';this.style.boxShadow='0 6px 20px rgba(249,132,0,0.4)'" onmouseout="this.style.background='linear-gradient(135deg,#f98400,#e67300)';this.style.transform='translateY(0)';this.style.boxShadow='0 4px 15px rgba(249,132,0,0.3)'">Submit Enquiry</button>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t\t</div>
\t\t\t\t\t\t\t\t\t\t\t\t\t</form>
\t\t\t\t\t\t\t\t\t\t\t\t\t</div>'''

if old_block in content:
    content = content.replace(old_block, new_form)
    print('iframe replaced with native form')
else:
    print('ERROR: exact block not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
with open('index.html', encoding='utf-8') as f:
    vcontent = f.read()

edumerge = vcontent.count('app.edumerge.com')
form_count = vcontent.count('admission-form')
fields = ['student_name', 'parent_name', 'email', 'phone', 'grade', 'academic_year', 'message']
print('edumerge refs:', edumerge)
print('form class count:', form_count)
for field in fields:
    print(field + ':', vcontent.count('name="' + field + '"'))
