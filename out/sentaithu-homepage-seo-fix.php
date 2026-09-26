<?php
/**
 * Sen Tài Thu — Homepage SEO fix
 * Dán vào: Snippets > Add New (plugin "Code Snippets"), chọn "Run snippet everywhere"
 * Hoặc: wp-content/themes/astra-child/functions.php
 *
 * KHÔNG dùng chung với Yoast/Rank Math (sẽ trùng thẻ). Nếu cài Rank Math thì
 * chỉ giữ lại hàm stt_fix_html_lang() và stt_homepage_jsonld().
 */

/* ---------- 1. lang="en-US" -> "vi-VN" ---------- */
add_filter( 'language_attributes', function ( $output ) {
	return 'lang="vi-VN"';
} );

/* ---------- 2. Title trang chủ ---------- */
add_filter( 'pre_get_document_title', function ( $title ) {
	if ( is_front_page() || is_home() ) {
		return 'Sen Tài Thu – Spa Trị Liệu Y Học Cổ Truyền Việt Nam | 15 Chi Nhánh';
	}
	return $title;
}, 20 );

/* ---------- 3. Meta description + Open Graph + Twitter Card ---------- */
add_action( 'wp_head', function () {
	if ( ! ( is_front_page() || is_home() ) ) {
		return;
	}

	$desc  = 'Sen Tài Thu – hơn 30 năm trị liệu Y học cổ truyền Việt Nam. Thăm khám bác sĩ Đông y, thủy trị liệu, xông hơi thảo dược, chườm ngải cứu. 15 chi nhánh tại Hà Nội, Đà Nẵng, TP.HCM. Hotline 1800 258 382.';
	$img   = 'https://sentaithu.com.vn/wp-content/uploads/2024/08/MT-6620.jpg';
	$url   = home_url( '/' );
	$title = 'Sen Tài Thu – Spa Trị Liệu Y Học Cổ Truyền Việt Nam | 15 Chi Nhánh';

	printf( '<meta name="description" content="%s" />' . "\n", esc_attr( $desc ) );
	printf( '<meta property="og:locale" content="vi_VN" />' . "\n" );
	printf( '<meta property="og:type" content="website" />' . "\n" );
	printf( '<meta property="og:site_name" content="Sen Tài Thu" />' . "\n" );
	printf( '<meta property="og:title" content="%s" />' . "\n", esc_attr( $title ) );
	printf( '<meta property="og:description" content="%s" />' . "\n", esc_attr( $desc ) );
	printf( '<meta property="og:url" content="%s" />' . "\n", esc_url( $url ) );
	printf( '<meta property="og:image" content="%s" />' . "\n", esc_url( $img ) );
	printf( '<meta property="og:image:width" content="1200" />' . "\n" );
	printf( '<meta property="og:image:height" content="630" />' . "\n" );
	printf( '<meta name="twitter:card" content="summary_large_image" />' . "\n" );
	printf( '<meta name="twitter:title" content="%s" />' . "\n", esc_attr( $title ) );
	printf( '<meta name="twitter:description" content="%s" />' . "\n", esc_attr( $desc ) );
	printf( '<meta name="twitter:image" content="%s" />' . "\n", esc_url( $img ) );
}, 1 );

/* ---------- 4. JSON-LD: Organization + WebSite + 15 chi nhánh ---------- */
add_action( 'wp_head', function () {
	if ( ! ( is_front_page() || is_home() ) ) {
		return;
	}

	$branches = array(
		// [ tên, đường, phường, thành phố, điện thoại ]
		array( 'Sen Tài Thu 1992', 'Tầng 11, Bệnh viện Châm cứu TW, 49 Thái Thịnh', 'Phường Đống Đa', 'Hà Nội', '+842432222386' ),
		array( 'Sen Tài Thu 110 Thái Thịnh', 'Tòa nhà Hacinco, 110 Thái Thịnh', 'Phường Đống Đa', 'Hà Nội', '+842435381199' ),
		array( 'Sen Tài Thu Thăng Long', '136 Phạm Văn Đồng', 'Phường Đông Ngạc', 'Hà Nội', '+842433941666' ),
		array( 'Sen Tài Thu Long Biên', 'Tầng 3 Đảo Sen, 125 Nguyễn Sơn', 'Phường Bồ Đề', 'Hà Nội', '+842433528989' ),
		array( 'Sen Tài Thu Trần Quốc Toản', '95 phố Hàng Lọng', 'Phường Cửa Nam', 'Hà Nội', '+842432239795' ),
		array( 'Sen Tài Thu Vincom Mega Mall Smart City', 'L2-12 Vincom Mega Mall Smart City', 'Phường Tây Mỗ', 'Hà Nội', '+842433597555' ),
		array( 'Sen Tài Thu Văn Cao', '39 Văn Cao', 'Phường Ngọc Hà', 'Hà Nội', '+842433661661' ),
		array( 'Sen Tài Thu Tây Hồ', 'Shophouse 03 & 04, Heritage West Lake, ngõ 677 Lạc Long Quân', 'Phường Tây Hồ', 'Hà Nội', '+84765677677' ),
		array( 'Sen Tài Thu Thái Bình', 'Tầng 4 Khách sạn Thái Bình Dream, 355 Lý Bôn, Tổ 11', 'Phường Trần Hưng Đạo', 'Hưng Yên', '+842276565599' ),
		array( 'Sen Tài Thu Đà Nẵng', '226 Võ Nguyên Giáp', 'Phường An Hải', 'Đà Nẵng', '+842363836888' ),
		array( 'Sen Tài Thu Tân Sơn Nhất', 'Tầng 3 Khách sạn Tân Sơn Nhất, 202 Hoàng Văn Thụ', 'Phường Đức Nhuận', 'Thành phố Hồ Chí Minh', '+842837977779' ),
		array( 'Sen Tài Thu Hà Nam', 'Tầng 5, Khách sạn Riverside, Lê Hoàn', 'Phường Phủ Lý', 'Ninh Bình', '+84818072288' ),
		array( 'Sen Tài Thu Lạng Sơn', 'Tầng 2, Imperial Hotel, 69 Lý Thường Kiệt, Phú Lộc 4', 'Phường Đông Kinh', 'Lạng Sơn', '+84964450089' ),
		array( 'Sen Tài Thu Hải Dương', '151 Hải An, Khu Đô Thị Ecopark', 'Hải Phòng', 'Hải Phòng', '+84703228888' ),
		array( 'Sen Tài Thu Bắc Ninh', 'H Hotel, 06 Ngô Tất Tố, Võ Cường', 'Bắc Ninh', 'Bắc Ninh', '+84832333000' ),
	);

	$hours = array(
		'@type'     => 'OpeningHoursSpecification',
		'dayOfWeek' => array( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ),
		'opens'     => '09:00',
		'closes'    => '22:00',
	);

	$departments = array();
	foreach ( $branches as $b ) {
		$departments[] = array(
			'@type'                       => 'HealthAndBeautyBusiness',
			'name'                        => $b[0],
			'image'                       => 'https://sentaithu.com.vn/wp-content/uploads/2024/08/MT-6620.jpg',
			'telephone'                   => $b[4],
			'priceRange'                  => '$$',
			'address'                     => array(
				'@type'           => 'PostalAddress',
				'streetAddress'   => $b[1],
				'addressLocality' => $b[2],
				'addressRegion'   => $b[3],
				'addressCountry'  => 'VN',
			),
			'openingHoursSpecification'   => array( $hours ),
			'parentOrganization'          => array( '@id' => 'https://sentaithu.com.vn/#organization' ),
		);
	}

	$graph = array(
		'@context' => 'https://schema.org',
		'@graph'   => array(
			array(
				'@type'       => 'Organization',
				'@id'         => 'https://sentaithu.com.vn/#organization',
				'name'        => 'Công Ty CP Tập Đoàn Sen Tài Thu Việt Nam',
				'alternateName' => 'Sen Tài Thu',
				'url'         => 'https://sentaithu.com.vn/',
				'logo'        => array(
					'@type' => 'ImageObject',
					'url'   => 'https://sentaithu.com.vn/wp-content/uploads/2024/08/Logo-STT-08-1.png',
				),
				'description' => 'Chuỗi spa trị liệu Y học cổ truyền Việt Nam với hơn 30 năm kinh nghiệm.',
				'address'     => array(
					'@type'           => 'PostalAddress',
					'streetAddress'   => 'Tầng 3, 136 Phạm Văn Đồng',
					'addressLocality' => 'Phường Đông Ngạc',
					'addressRegion'   => 'Hà Nội',
					'addressCountry'  => 'VN',
				),
				'contactPoint' => array(
					array(
						'@type'             => 'ContactPoint',
						'telephone'         => '+84906169926',
						'contactType'       => 'sales',
						'availableLanguage' => array( 'Vietnamese' ),
					),
					array(
						'@type'             => 'ContactPoint',
						'telephone'         => '1800258382',
						'contactType'       => 'customer service',
						'availableLanguage' => array( 'Vietnamese' ),
					),
				),
				'sameAs'     => array(
					// TODO: thay bằng URL thật của Fanpage / Youtube / Twitter
					'https://www.facebook.com/sentaithu',
					'https://www.youtube.com/@sentaithu',
				),
				'department' => $departments,
			),
			array(
				'@type'     => 'WebSite',
				'@id'       => 'https://sentaithu.com.vn/#website',
				'url'       => 'https://sentaithu.com.vn/',
				'name'      => 'Sen Tài Thu',
				'inLanguage' => 'vi-VN',
				'publisher' => array( '@id' => 'https://sentaithu.com.vn/#organization' ),
				'potentialAction' => array(
					'@type'       => 'SearchAction',
					'target'      => array(
						'@type'       => 'EntryPoint',
						'urlTemplate' => 'https://sentaithu.com.vn/?s={search_term_string}',
					),
					'query-input' => 'required name=search_term_string',
				),
			),
		),
	);

	echo '<script type="application/ld+json">'
		. wp_json_encode( $graph, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES )
		. '</script>' . "\n";
}, 2 );

/* ---------- 5. Dọn rác WordPress lộ ra ở <head> ---------- */
remove_action( 'wp_head', 'wp_generator' );
remove_action( 'wp_head', 'rsd_link' );
remove_action( 'wp_head', 'wlwmanifest_link' );
remove_action( 'wp_head', 'feed_links_extra', 3 );

/* ---------- 6. Bỏ sitemap tác giả (wp-sitemap-users-1.xml) ---------- */
add_filter( 'wp_sitemaps_add_provider', function ( $provider, $name ) {
	return ( 'users' === $name ) ? false : $provider;
}, 10, 2 );
