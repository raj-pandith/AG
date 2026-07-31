import os
import re

# The correct mobile menu block from mainfolder.com/index.html (lines 269-370)
correct_menu = """    <!--==============================Mobile Menu============================== -->
    <div class="th-menu-wrapper onepage-nav">
        <div class="th-menu-area text-center">
            <button class="th-menu-toggle"><i class="fal fa-times"></i></button>
            <div class="mobile-logo">
                <a href="index.html">
                    <!-- <img src="assets/ojixs/logo/nav-logo.png" data-original-src="assets/img/logo2.svg"
                        alt="jhs"> -->

                    <img src="assets/ojixs/logo/nav-logo.png" data-original-src="assets/img/logo2.svg" alt="jhs">
                </a>
            </div>
            <div class="th-mobile-menu">
                <ul>
                    <li class="mega-menu-wrap">
                        <a class="active" href="index.html">Home</a>
                    </li>

                    <li class="menu-item-has-children">
                        <a href="#">About Us</a>
                        <ul class="sub-menu">
                            <li><a href="ourhistory.html">Our History</a></li>
                            <li><a href="vision-mission.html">Vision and Mission</a></li>
                            <li><a href="chairmans-message.html">Chairman Message</a></li>
                            <li><a href="careers.html">Careers</a></li>
                        </ul>
                    </li>

                    <li class="menu-item-has-children">
                        <a href="#">Academics</a>
                        <ul class="sub-menu">
                            <li><a href="cbse-affiliation.html">CBSE Affiliation</a></li>
                            <li><a href="list-of-prescribed-books.html">List of Prescribe Books</a></li>
                            <li><a href="no-homework-policy.html">No HomeWork Policy</a>
                            </li>
                            <li><a href="institution-tieups.html">Institution tieup</a></li>
                        </ul>
                    </li>
                    <li class="menu-item-has-children">
                        <a href="#">Admissions</a>
                        <ul class="sub-menu">
                            <li><a href="eligibility-and-essential-documents.html">Eligibility-and-essential-documents</a>
                            </li>
                            <li><a href="schedule-an-interaction.html">Schedule an interaction</a></li>
                            <li><a href="admission-forms.html">Admission Forms</a></li>
                            <li><a href="assets/pdf/Fees%20Structure.pdf" target="_blank">Fees structure</a></li>
                            <li><a href="assets/pdf/Refund_policy.pdf" target="_blank">Refund Policy</a></li>
                            <li><a href="admissions-2026-27/application/index.html" target="_blank">Enquiry now</a></li>
                        </ul>
                    </li>
                    <li class="menu-item-has-children">
                        <a href="#">Media & Insites</a>
                        <ul class="sub-menu">
                            <li><a href="mandatory-disclosure.html">Mandatory disclosure</a></li>
                            <li><a href="tempo-event.html">News and Events</a></li>
                            <li><a href="gallery.html">Photo and Video Gallery</a></li>
                            <li><a href="newsletter.html">Newsletter</a></li>
                            <li><a href="press-release.html">Press Release</a></li>
                            <li><a href="blog-grid.html">Blogs</a></li>
                            <li><a href="faq.html">FAQ</a></li>
                        </ul>
                    </li>
                    <li class="menu-item-has-children">
                        <a href="#">Life at AG</a>
                        <ul class="sub-menu">
                            <li class="menu-item-has-children">
                                <a href="#">Learning</a>
                                <ul class="sub-menu">
                                    <li><a href="learning-resource-center.html">Learning Resource Center</a></li>
                                    <li><a href="learning-labs.html">Learnning Labs</a>
                                    </li>
                                    <li><a href="art-and-finearts-studio.html">Art & Fine Arts Studio</a></li>
                                </ul>
                            </li>
                            <li class="menu-item-has-children">
                                <a href="#">Compus Life</a>
                                <ul class="sub-menu">
                                    <li><a href="transportation.html">Transportation</a></li>
                                    <li><a href="meal-plan.html">Meal Plan</a></li>
                                    <li><a href="health-services.html">Health Service</a></li>
                                    <li><a href="circle-time.html">Circle time</a></li>
                                </ul>
                            </li>
                            <li class="menu-item-has-children">
                                <a href="#">Holistic Learning</a>
                                <ul class="sub-menu">
                                    <li><a href="clubs.html">Clubs</a></li>
                                    <li><a href="supplymentary-activities.html">Suplymentary Activities</a></li>
                                    <li><a href="field-trips.html">Field Trips</a></li>
                                    <li><a href="summer-camp-and-sports-training.html">Summer Camp & Sports Traning</a>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li class="mega-menu-wrap">
                        <a href="contact-us.html">Contact Us</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>

"""

# Pattern to find start of mobile menu block (handles both formats with/without spaces)
mobile_menu_start = re.compile(r'<!--=+\s*Mobile Menu\s*=+', re.IGNORECASE)

# Pattern to find Header Area comment that follows the mobile menu block
header_area_start = re.compile(r'<!--=+\s*Header Area\s*=+', re.IGNORECASE)

base_dir = r'c:\My Web Sites\Jain2'

# Find all target HTML files
target_files = []
skipped = []

for folder in ['ag.com', 'mainfolder.com']:
    folder_path = os.path.join(base_dir, folder)
    if not os.path.isdir(folder_path):
        continue
    for root, dirs, files in os.walk(folder_path):
        for fname in sorted(files):
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, base_dir)
            # Skip the source file
            if rel == os.path.join('mainfolder.com', 'index.html'):
                skipped.append(rel)
                continue
            # Check if file has mobile menu
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if mobile_menu_start.search(content):
                    target_files.append(fpath)
            except Exception:
                pass

print(f"Source file skipped: mainfolder.com/index.html")
print(f"Found {len(target_files)} files with mobile menus to update\n")

updated = 0
errors = 0
error_files = []

for fpath in target_files:
    rel = os.path.relpath(fpath, base_dir)
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find start of mobile menu block
        start_match = mobile_menu_start.search(content)
        if not start_match:
            continue

        # Find the Header Area comment that follows
        header_match = header_area_start.search(content, start_match.end())
        if not header_match:
            print(f"  WARNING: No Header Area found after mobile menu in {rel}")
            errors += 1
            error_files.append(rel)
            continue

        # Replace the old mobile menu block with the correct one
        new_content = content[:start_match.start()] + correct_menu + content[header_match.start():]

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        updated += 1
        print(f"  Updated: {rel}")

    except Exception as e:
        print(f"  ERROR in {rel}: {e}")
        errors += 1
        error_files.append(rel)

print(f"\n{'='*60}")
print(f"Total files updated: {updated}")
print(f"Errors: {errors}")
if error_files:
    print(f"Files with errors: {error_files}")
